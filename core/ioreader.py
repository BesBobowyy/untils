from core.utils.type_aliases import UnknownConfigType, ConfigSupportedExtensions
from core.iovalidator import IOValidator
from core.utils.protocols import IOReaderMixin

from core.settings import Settings

from typing import Dict

import json
import os

class JSONMixin:
    """JSON extension for IOReader."""

    @staticmethod
    def read(settings: Settings, file_path: str) -> UnknownConfigType:
        with open(file_path, 'r', encoding='utf-8') as file:
            content: UnknownConfigType = json.loads(file.read())
        return content

class IOReader():
    """This class works with config files in supported formats."""

    _MIXINS: Dict[ConfigSupportedExtensions, IOReaderMixin] = {
        ".json": JSONMixin,
        ".json5": JSONMixin
    }

    @staticmethod
    def read_file(settings: Settings, file_path: str):
        IOValidator.validate_config_path(settings, file_path)

        extension: str = os.path.splitext(file_path)[1]
        content: UnknownConfigType = {}

        if extension in IOReader._MIXINS:
            content: UnknownConfigType = IOReader._MIXINS[extension].read(settings, file_path)
        
        return content



if __name__ == "__main__":
    PATH: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    FILE_PATH: str = os.path.join(PATH, "examples", "resources", "commands_1.json")
    print(PATH, FILE_PATH)
    print(IOReader.read_file(Settings(), FILE_PATH))