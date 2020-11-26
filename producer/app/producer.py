"""Send website scrape / ping results ot a kafka topic

> The website checker should perform the checks periodically and collect the
> HTTP response time, error code returned, as well as optionally checking the
> returned page contents for a regexp pattern that is expected to be found on the
> page.

"""

# This is initially based on the examples from https://towardsdatascience.com/kafka-docker-python-408baf0e1088

from kafka import KafkaProducer
from . import config as c
import json
import time


def main():
    producer = KafkaProducer(
        bootstrap_servers=[c.KAFKA_BOOTSTRAP_SERVER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    for i in range(100):
        # seconds since epoch 1970-01-01
        # Might be different epoch an different platforms -> ignored for now
        ts = time.time()
        producer.send(c.KAFKA_TOPIC,
                      value={'timestamp': ts,
                             'url': 'https://google.com',
                             'response_time_seconds': float(i),
                             'status_code': 200,
                             'found_regex_pattern': True}
                      )
        print(f'Send {i}')
        time.sleep(c.PRODUCER_INTERVAL_SECONDS)
