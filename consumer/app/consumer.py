"""Send website scrape / ping results ot a kafka topic

> For the database writer we expect to see a solution that records the check
> results into one or more database tables and could handle a reasonable amount
> of checks performed over a longer period of time.


"""

# This is initially based on the examples from https://towardsdatascience.com/kafka-docker-python-408baf0e1088

from kafka import KafkaConsumer
from . import config
import json
from . import postgres as pg
import datetime
import time


def main():
    migrate_db()
    c = config.load_config()
    consumer = KafkaConsumer(
        c.KAFKA_TOPIC,
        bootstrap_servers=[c.KAFKA_BOOTSTRAP_SERVER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='consumer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    # works as an endless loop
    for event in consumer:
        event_data = event.value
        # {
        #  'timestamp': ..., # float, seconds since epoch
        #  'url': 'https://google.com', # str, url
        #  'response_time_seconds': ..., # float, seconds
        #  'status_code': 200, # int
        #  'found_regex_pattern': True # bool
        #  }
        print(event_data)

        # "validate": at least make sure it fits the spec and all data is there
        validated_data = {}
        try:
            # always pass in a tz! https://blog.ganssle.io/articles/2019/11/utcnow.html
            validated_data['timestamp'] = datetime.datetime.fromtimestamp(event_data['timestamp'],
                                                                          tz=datetime.timezone.utc)
            validated_data['url'] = str(event_data['url'])
            validated_data['response_time_seconds'] = float(event_data['response_time_seconds'])
            validated_data['status_code'] = int(event_data['status_code'])
            validated_data['found_regex_pattern'] = bool(event_data['found_regex_pattern'])
        except KeyError as e:
            print(f"{e!r}: ignoring event: {event_data}")
            continue

        with pg.postgres_cursor_context() as cursor:
            cursor.execute(f"""
                INSERT INTO content(timestamp, url, response_time_seconds, status_code, found_regex_pattern)
                VALUES (%(timestamp)s, %(url)s, %(response_time_seconds)s, %(status_code)s, %(found_regex_pattern)s);
            """, validated_data)


def migrate_db():
    """Creates the required tables"""
    # I know, crude, but it works...
    # v0
    try:
        with pg.postgres_cursor_context() as cursor:
            cursor.execute("""
CREATE TABLE public.content(
timestamp             TIMESTAMPTZ,
url                   TEXT,
response_time_seconds DOUBLE PRECISION,
status_code           SMALLINT,
found_regex_pattern   BOOLEAN
);
""")
    except Exception as e:
        # expected when we are already at v0
        print(repr(e))

