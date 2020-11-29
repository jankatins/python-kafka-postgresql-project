"""Send website scrape / ping results ot a kafka topic

> The website checker should perform the checks periodically and collect the
> HTTP response time, error code returned, as well as optionally checking the
> returned page contents for a regexp pattern that is expected to be found on the
> page.

"""

# This is initially based on the examples from https://towardsdatascience.com/kafka-docker-python-408baf0e1088

import itertools
import json
import re
import time
import typing as t

import httpx
from kafka import KafkaProducer

from . import config
from . import check_event


def main():
    """Runs the producer with the given configuration"""
    c = config.load_config()
    auth_kwargs = {}
    if c.KAFKA_CERT_PATH:
        cert_path = c.KAFKA_CERT_PATH
        auth_kwargs.update(dict(
            security_protocol="SSL",
            ssl_cafile=f"{cert_path}/ca.pem",
            ssl_certfile=f"{cert_path}/service.cert",
            ssl_keyfile=f"{cert_path}/service.key",
        ))
    producer = KafkaProducer(
        bootstrap_servers=[c.KAFKA_BOOTSTRAP_SERVER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        **auth_kwargs
    )
    max_loops = c.PRODUCER_MAX_LOOPS
    wait_between_scrapes = c.PRODUCER_INTERVAL_SECONDS
    kafka_topic = c.KAFKA_TOPIC

    url = c.PRODUCER_SCRAPE_URL
    if c.PRODUCER_SCRAPE_REGEX:
        regex = re.compile(c.PRODUCER_SCRAPE_REGEX)
    else:
        regex = None
    print(f'Configured URL: {url}, regex: {c.PRODUCER_SCRAPE_REGEX}')

    run_producer(producer, kafka_topic, max_loops, wait_between_scrapes, url, regex)


def run_producer(kafka_producer: KafkaProducer,
                 kafka_topic: str,
                 max_loops: t.Optional[int],
                 wait_between_scrapes: int,
                 url: str,
                 regex: t.Optional[re.Pattern] = None,
                 ):
    """Checks the website in a loop and sends events out via Kafka

    The Event conforms to the `checkweb.check_event.CheckEvent` dataclass.

    :type kafka_producer: KafakProducer instance
    :param kafka_topic: The kafka topic to send the events to
    :param max_loops: max numbers of times to check the website
    :param wait_between_scrapes: waiting time in seconds between checks
    :param url: the URL to check
    :param regex: The regex pattern to check the content for
    """

    if max_loops > 0:
        loop_iter = range(0, max_loops)
    else:
        loop_iter = itertools.count(0)

    for i in loop_iter:
        # seconds since epoch 1970-01-01
        # Might be different epoch an different platforms -> ignored for now
        event = check_website(url, regex)
        kafka_producer.send(kafka_topic, value=event.to_dict())
        print(f'Send {i}: {event}')
        time.sleep(wait_between_scrapes)


def check_website(url: str, regex: t.Optional[re.Pattern]) -> check_event.CheckEvent:
    """Check website for pattern

    :param url: the URL to check
    :param regex: The regex pattern to check the content for
    :return: `CheckEvent` instance which contains the result of the check
    """
    ts_before = time.time()
    exception_message = ""
    found_regex_pattern = None
    status_code = None
    try:
        r = httpx.get(url)
        if regex:
            found_regex_pattern = bool(regex.search(r.text, re.MULTILINE))
        status_code = r.status_code
    except Exception as e:
        # e.g. a timeout or a DNS problem -> send the exception on so it can be investigated
        exception_message = repr(e)
    ts_after = time.time()
    # print(f'Response text: {r.text}')
    event = check_event.CheckEvent(
        timestamp=ts_before,
        url=url,
        response_time_seconds=ts_after - ts_before,
        status_code=status_code,
        found_regex_pattern=found_regex_pattern,
        exception_message=exception_message
    )

    return event
