"""Central place to setup needed config

All config via environment variables for now
"""
import os

KAFKA_BOOTSTRAP_SERVER=f"{os.environ['KAFKA_BOOTSTRAP_SERVER']}"
KAFKA_TOPIC=f"{os.environ['KAFKA_TOPIC']}"

PRODUCER_INTERVAL_SECONDS=int(f"{os.environ['PRODUCER_INTERVAL_SECONDS']}")
PRODUCER_SCRAPE_URL=f"{os.environ['PRODUCER_SCRAPE_URL']}"
PRODUCER_SCRAPE_REGEX=f"{os.environ['PRODUCER_SCRAPE_REGEX']}"
# 0 = don't stop
PRODUCER_MAX_LOOPS=int(f"{os.environ.get('PRODUCER_MAX_LOOPS', 0)}")
