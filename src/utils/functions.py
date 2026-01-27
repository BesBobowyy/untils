"""functions.py - Useful functions."""

import warnings

from typing import Type, Optional, Tuple, Union

from src.utils.enums import WarningsLevel

from src.settings import Settings
from src.utils.lib_warnings import (
    FileWarning, ConfigWarning, InputWarning, FileError, ConfigError, InputError
)

def warning(
    settings: Settings,
    message: str,
    auto_correct: str,
    warning_type: Type[Union[FileWarning, ConfigWarning, InputWarning]]=ConfigWarning,
    exception_type: Type[Union[FileError, ConfigError, InputError]]=ConfigError,
    warning_levels: Optional[Union[Tuple[WarningsLevel, ...], Tuple[None]]]=None,
    exception_levels: Optional[Union[Tuple[WarningsLevel, ...], Tuple[None]]]=None
) -> None:
    """Warning or exception in validators."""

    if settings.warnings_level in (warning_levels or (WarningsLevel.BASIC,)):
        settings.logger.warning(message + ' ' + auto_correct, stacklevel=3)
        warnings.warn(
            message + ' ' + auto_correct,
            warning_type,
            stacklevel=3
        )
    elif settings.warnings_level in (exception_levels or (WarningsLevel.STRICT,)):
        settings.logger.error(message, stacklevel=3)
        raise exception_type(message)
