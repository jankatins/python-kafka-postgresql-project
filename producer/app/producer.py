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

import httpx
from kafka import KafkaProducer

from . import config as c


def main():
    producer = KafkaProducer(
        bootstrap_servers=[c.KAFKA_BOOTSTRAP_SERVER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    url = c.PRODUCER_SCRAPE_URL
    regex = re.compile(c.PRODUCER_SCRAPE_REGEX)
    print(f'Configured URL: {url}, regex: {c.PRODUCER_SCRAPE_REGEX}')
    max_loops = c.PRODUCER_MAX_LOOPS

    if max_loops > 0:
        loop_iter = range(0, max_loops)
    else:
        loop_iter = itertools.count(0)


    for i in loop_iter:
        # seconds since epoch 1970-01-01
        # Might be different epoch an different platforms -> ignored for now
        ts_before = time.time()
        r = httpx.get(url)
        ts_after = time.time()
        found_regex_pattern = bool(regex.search(r.text, re.MULTILINE))
        #print(f'Response text: {r.text}')
        event = {
            'timestamp': ts_before,
            'url': url,
            'response_time_seconds': ts_after - ts_before,
            'status_code': r.status_code,
            'found_regex_pattern': found_regex_pattern
        }
        producer.send(c.KAFKA_TOPIC, value=event)
        print(f'Send {i}: {event}')
        time.sleep(c.PRODUCER_INTERVAL_SECONDS)
