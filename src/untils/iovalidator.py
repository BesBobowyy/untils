"""iovalidator.py - `IOValidator` for IO validations."""

# pylint: disable=too-few-public-methods

import os

from untils.utils.enums import WarningsLevel
from untils.utils.constants import Constants, Strings
from untils.utils.lib_warnings import FileWarning, FileError

from untils.settings import Settings

class IOValidator:
    """Validator class for the all IO operations for `IOReader`."""

    @staticmethod
    def validate_config_path(settings: Settings, file_path: str) -> bool:
        """Validates a config path.
        
        Args:
            settings: The settings.
            file_path: The file path.

        Returns:
            `True` if the config path is valid and supported, else `False`.

        Raises:
            FileWarning: The config file is not exists or the config extension is not in standart.

            FileError: The config file is not exists.
        """

        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Processing the config file path.
            extension: str = os.path.splitext(file_path)[1]
            if extension in Constants.SUPPORTED_CONFIG_FORMATS:
                if extension not in Constants.STANDART_CONFIG_FORMATS:
                    # The config format is not in standart.
                    settings.warning(
                        Strings.CONFIG_EXTENSION_NOT_SUPPORTS,
                        Strings.AUTO_CORRECT_WITH_ACCEPTING,
                        FileWarning,
                        warning_levels=(WarningsLevel.BASIC, WarningsLevel.STRICT),
                        exception_levels=()
                    )
                return True
        else:
            settings.warning(
                Strings.CONFIG_FILE_NOT_EXISTS,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                FileWarning,
                FileError
            )

        return False
