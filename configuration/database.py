from configparser import ConfigParser
from typing import Optional

from configuration.config import ConfigurationOption

DATABASE_KEY = 'Database'


class DatabaseUser(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'PostgresUser')


class DatabasePassword(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'PostgresPassword')


class DatabaseHost(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'PostgresHost')


class DatabasePort(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'PostgresPort')


class DatabaseName(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> Optional[str]:
        return configuration.get(DATABASE_KEY, 'PostgresDB')
