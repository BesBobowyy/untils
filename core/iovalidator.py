from core.utils.enums import WarningsLevel
from core.utils.constants import Constants, Strings
from core.utils.lib_warnings import FileWarning, FileError
from core.utils.functions import warning

from core.settings import Settings

import os

class IOValidator:
    """Validator class for IO operations."""

    @staticmethod
    def validate_config_path(settings: Settings, file_path: str) -> bool:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            extension: str = os.path.splitext(file_path)[1]
            if extension in Constants.SUPPORTED_CONFIG_FORMATS:
                if extension not in Constants.STANDART_CONFIG_FORMATS:
                    warning(
                        settings,
                        Strings.CONFIG_EXTENSION_NOT_SUPPORTS,
                        Strings.AUTO_CORRECT_WITH_ACCEPTING,
                        FileWarning,
                        warning_levels=(WarningsLevel.Basic, WarningsLevel.Strict),
                        exception_levels=()
                    )
                return True
        else:
            warning(
                settings,
                Strings.CONFIG_FILE_NOT_EXISTS,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                FileWarning,
                FileError
            )
        
        return False