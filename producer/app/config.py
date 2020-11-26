"""Central place to setup needed config

All config via environment variables for now
"""
import os

KAFKA_BOOTSTRAP_SERVER=f"{os.environ['KAFKA_BOOTSTRAP_SERVER']}"
KAFKA_TOPIC=f"{os.environ['KAFKA_TOPIC']}"

PRODUCER_INTERVAL_SECONDS=int(f"{os.environ['PRODUCER_INTERVAL_SECONDS']}")

