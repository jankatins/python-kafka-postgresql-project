"""Central place to setup needed config

All config via environment variables for now
"""
import os

_config_cache = None


# make it a real class to help the IDE...
class ConsumerConfig():
    def __init__(self):
        self.KAFKA_BOOTSTRAP_SERVER = f"{os.environ['KAFKA_BOOTSTRAP_SERVER']}"
        self.KAFKA_TOPIC = f"{os.environ['KAFKA_TOPIC']}"
        self.CONSUMER_POSTGRES_USER = f"{os.environ['CONSUMER_POSTGRES_USER']}"
        self.CONSUMER_POSTGRES_PASSWORD = f"{os.environ['CONSUMER_POSTGRES_PASSWORD']}"
        self.CONSUMER_POSTGRES_DB = f"{os.environ['CONSUMER_POSTGRES_DB']}"
        self.CONSUMER_POSTGRES_HOST = f"{os.environ.get('CONSUMER_POSTGRES_HOST', 'db')}"
        self.CONSUMER_POSTGRES_PORT = int(f"{os.environ.get('CONSUMER_POSTGRES_PORT', '5432')}")


def load_config() -> ConsumerConfig:
    global _config_cache
    if not _config_cache:
        _config_cache = ConsumerConfig()
    return _config_cache
