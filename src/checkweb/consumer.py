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
    auth_kwargs = {}
    if c.KAFKA_CERT_PATH:
        cert_path = c.KAFKA_CERT_PATH
        auth_kwargs.update(dict(
            security_protocol="SSL",
            ssl_cafile=f"{cert_path}/ca.pem",
            ssl_certfile=f"{cert_path}/service.cert",
            ssl_keyfile=f"{cert_path}/service.key",
        ))
    consumer = KafkaConsumer(
        c.KAFKA_TOPIC,
        bootstrap_servers=[c.KAFKA_BOOTSTRAP_SERVER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='consumer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        **auth_kwargs
    )
    # works as an endless loop
    for event in consumer:
        event_data = event.value
        handle_event_dict(event_data)

def handle_event_dict(event_data: dict):
    """ Handle a single event and save it to the database

    :param event_data: a dict which needs to be convertible to a CheckEvent. data not convertable will be logged and ignored
    """
    try:
        # does some validation
        event = check_event.CheckEvent.from_dict(event_data)
    except RuntimeError as e:
        print(f"{e!r}: ignoring event: {event_data}")
        return

    print(f"Consuming event: {event}")

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
