import os

from loguru import logger as lo
from pyhocon import ConfigFactory


class HoconConfig:
    def __init__(self, filename="./config.conf"):
        self.data = self.__load_config(filename)

    def __load_config(self, filename):
        config_path = os.environ.get("CONFIG_URL", filename).strip()

        lo.info(f"Loading config from {config_path}")
        if config_path.startswith("http://") or config_path.startswith("https://"):
            timeout = int(os.environ.get("DEFAULT_CONFIG_TIMEOUT", 5))
            data = ConfigFactory.parse_URL(config_path, timeout=timeout)
        else:
            data = ConfigFactory.parse_file(config_path)
        assert isinstance(data, dict)
        return data

    def get(self, key, default=None):
        return self.data.get(key, default)


config = HoconConfig(filename="./config.conf")