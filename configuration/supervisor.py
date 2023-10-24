from configparser import ConfigParser

from configuration.config import ConfigurationOption

SUPERVISOR_KEY = 'SuperVisor'


class SupervisorName(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> str | None:
        return configuration.get(SUPERVISOR_KEY, 'Name')


class SupervisorPassword(ConfigurationOption):
    @staticmethod
    def get_value(configuration: ConfigParser) -> str | None:
        return configuration.get(SUPERVISOR_KEY, 'Password')
