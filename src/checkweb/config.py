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
        self.KAFKA_CERT_PATH = os.environ.get('KAFKA_CERT_PATH', None)

        # A bit too forgiving for my taste, but it will error in other places if a config is undefined...
        # Should have probably gone for a .env config solution...
        try:
            self.PRODUCER_INTERVAL_SECONDS = int(f"{os.environ['PRODUCER_INTERVAL_SECONDS']}")
            self.PRODUCER_SCRAPE_URL = f"{os.environ['PRODUCER_SCRAPE_URL']}"
            # regex checking is optional
            self.PRODUCER_SCRAPE_REGEX = f"{os.environ.get('PRODUCER_SCRAPE_REGEX','')}"
            # 0 = don't stop
            self.PRODUCER_MAX_LOOPS = int(f"{os.environ.get('PRODUCER_MAX_LOOPS', 0)}")
        except KeyError as e:
            print(f"Missing configuration for PRODUCER: {e!r}")

        try:
            self.CONSUMER_POSTGRES_USER = f"{os.environ['CONSUMER_POSTGRES_USER']}"
            self.CONSUMER_POSTGRES_PASSWORD = f"{os.environ['CONSUMER_POSTGRES_PASSWORD']}"
            self.CONSUMER_POSTGRES_DB = f"{os.environ['CONSUMER_POSTGRES_DB']}"
            self.CONSUMER_POSTGRES_HOST = f"{os.environ.get('CONSUMER_POSTGRES_HOST', 'db')}"
            self.CONSUMER_POSTGRES_PORT = int(f"{os.environ.get('CONSUMER_POSTGRES_PORT', '5432')}")
            self.CONSUMER_POSTGRES_SSL_MODE = os.environ.get('CONSUMER_POSTGRES_SSL_MODE', None)
        except KeyError as e:
            print(f"Missing configuration for CONSUMER: {e!r}")


def load_config() -> ProducerConfig:
    global _config_cache
    if not _config_cache:
        _config_cache = ProducerConfig()
    return _config_cache

