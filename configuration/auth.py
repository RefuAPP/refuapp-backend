from configparser import ConfigParser
from typing import Optional

from configuration.config import ConfigurationOption

AUTH_KEY = 'Auth'


class SecretKeyToken(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(AUTH_KEY, 'SecretKey')


class Algorithm(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(AUTH_KEY, 'Algorithm')
