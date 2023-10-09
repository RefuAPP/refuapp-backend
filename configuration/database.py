from configparser import ConfigParser
from typing import Optional

from configuration.config import ConfigurationOption

DATABASE_KEY = 'Database'


class DatabaseUrl(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'Url')
