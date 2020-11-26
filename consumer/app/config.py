"""Central place to setup needed config

All config via environment variables for now
"""
import os

KAFKA_BOOTSTRAP_SERVER=f"{os.environ['KAFKA_BOOTSTRAP_SERVER']}"
KAFKA_TOPIC=f"{os.environ['KAFKA_TOPIC']}"

CONSUMER_POSTGRES_USER=f"{os.environ['CONSUMER_POSTGRES_USER']}"
CONSUMER_POSTGRES_PASSWORD=f"{os.environ['CONSUMER_POSTGRES_PASSWORD']}"
CONSUMER_POSTGRES_DB=f"{os.environ['CONSUMER_POSTGRES_DB']}"
CONSUMER_POSTGRES_HOST=f"{os.environ.get('CONSUMER_POSTGRES_HOST', 'db')}"
CONSUMER_POSTGRES_PORT=int(f"{os.environ.get('CONSUMER_POSTGRES_PORT', '5432')}")


