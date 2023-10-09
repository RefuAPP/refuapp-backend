import configparser
from abc import ABC, abstractmethod
from typing import Optional, Type
import os


class ConfigurationOption(ABC):
    @staticmethod
    @abstractmethod
    def get_value(configuration: configparser.ConfigParser) -> Optional[str]:
        pass


class Configuration:
    CONFIG = None
    CONFIGURATION_FILE = "config.ini"

    @staticmethod
    def set_up():
        if Configuration.CONFIG is None:
            Configuration.__instantiate__()
        return Configuration.CONFIG

    @staticmethod
    def __instantiate__():
        Configuration.CONFIG = configparser.ConfigParser(os.environ)
        Configuration.CONFIG.read(Configuration.CONFIGURATION_FILE)

    @staticmethod
    def get(option: Type[ConfigurationOption]):
        Configuration.set_up()
        return option().get_value(configuration=Configuration.CONFIG)  # type: ignore
