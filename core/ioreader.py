from core.utils.type_aliases import UnknownConfigType, ConfigSupportedExtensions
from core.iovalidator import IOValidator
from core.utils.protocols import IOReaderMixin, IOReaderProtocol

from core.settings import Settings

from typing import Dict, override

import json
import os

class JSONMixin(IOReaderMixin):
    """The JSON extension for `IOReader`."""

    @override
    @staticmethod
    def read(settings: Settings, file_path: str) -> UnknownConfigType:
        with open(file_path, 'r', encoding='utf-8') as file:
            content: UnknownConfigType = json.loads(file.read())
        return content

class IOReader():
    """Reader class for config loading by paths and settings."""

    _MIXINS: Dict[ConfigSupportedExtensions, IOReaderProtocol] = {
        ".json": JSONMixin,
        ".json5": JSONMixin
    }
    """All supported mixins for `IOReader`."""

    @staticmethod
    def read_file(settings: Settings, file_path: str) -> UnknownConfigType:
        """Reads a config file by path.
        
        Args:
            settings: The settings.
            file_path: The file path.

        Returns:
            The raw unvalidated config.
        """

        IOValidator.validate_config_path(settings, file_path)

        extension: str = os.path.splitext(file_path)[1]
        content: UnknownConfigType = {}

        if extension in IOReader._MIXINS:
            content: UnknownConfigType = IOReader._MIXINS[extension].read(settings, file_path)
        
        return content