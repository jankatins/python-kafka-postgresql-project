"""Central place to setup needed config

All config via environment variables for now
"""
import os

_config_cache = None

# make it a real class to help the IDE...
class ProducerConfig():
    def __init__(self):
        self.KAFKA_BOOTSTRAP_SERVER = f"{os.environ['KAFKA_BOOTSTRAP_SERVER']}"
        self.KAFKA_TOPIC = f"{os.environ['KAFKA_TOPIC']}"
        self.PRODUCER_INTERVAL_SECONDS = int(f"{os.environ['PRODUCER_INTERVAL_SECONDS']}")
        self.PRODUCER_SCRAPE_URL = f"{os.environ['PRODUCER_SCRAPE_URL']}"
        self.PRODUCER_SCRAPE_REGEX = f"{os.environ['PRODUCER_SCRAPE_REGEX']}"
        # 0 = don't stop
        self.PRODUCER_MAX_LOOPS = int(f"{os.environ.get('PRODUCER_MAX_LOOPS', 0)}")


def load_config() -> ProducerConfig:
    global _config_cache
    if not _config_cache:
        _config_cache = ProducerConfig()
    return _config_cache

