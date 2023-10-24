from configparser import ConfigParser

from configuration.config import ConfigurationOption

ADMIN_KEY = 'Admin'


class AdminName(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> str | None:
        return configuration.get(ADMIN_KEY, 'Name')


class AdminPassword(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> str | None:
        return configuration.get(ADMIN_KEY, 'Password')
