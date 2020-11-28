"""Send website scrape / ping results ot a kafka topic

> For the database writer we expect to see a solution that records the check
> results into one or more database tables and could handle a reasonable amount
> of checks performed over a longer period of time.


"""

# This is initially based on the examples from https://towardsdatascience.com/kafka-docker-python-408baf0e1088

import datetime
import json

from kafka import KafkaConsumer

from . import config
from . import check_event
from . import postgres as pg


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

        # does some validation
        try:
            event = check_event.CheckEvent.from_dict(event_data)

        except (RuntimeError, AssertionError) as e:
            print(f"{e!r}: ignoring event: {event_data}")
            continue

        with pg.postgres_cursor_context() as cursor:
            cursor.execute(f"""
                INSERT INTO content(timestamp, url, response_time_seconds, status_code, found_regex_pattern, exception_message, version)
                VALUES 
                (%(timestamp)s, %(url)s, %(response_time_seconds)s, %(status_code)s, %(found_regex_pattern)s, %(exception_message)s, %(version)s)
                ;
            """, event.to_database_dict())


def migrate_db():
    """Creates the required tables"""
    # I know, crude, but it works...
    # v0
    with pg.postgres_cursor_context() as cursor:
        cursor.execute("""
CREATE TABLE IF NOT EXISTS public.content(
timestamp             TIMESTAMPTZ,
url                   TEXT,
response_time_seconds DOUBLE PRECISION,
status_code           SMALLINT,
found_regex_pattern   BOOLEAN
);
""")

    with pg.postgres_cursor_context() as cursor:
        cursor.execute("""
-- don't block for too long in rolling upgrades
SET lock_timeout TO '15s';
ALTER TABLE public.content ADD COLUMN IF NOT EXISTS exception_message TEXT NULL;
-- requires pg11 
ALTER TABLE public.content ADD COLUMN IF NOT EXISTS version SMALLINT NOT NULL DEFAULT 0;
""")
