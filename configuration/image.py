from configparser import ConfigParser
from typing import Optional

from configuration.config import ConfigurationOption

IMAGE_KEY = 'Image'


class DefaultImage(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(IMAGE_KEY, 'Default')
