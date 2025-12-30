from core.utils.enums import WarningsLevel

from core.settings import Settings

from typing import Type, Optional, Tuple, Union

import warnings

def warning(
    settings: Settings,
    message: str,
    auto_correct: str,
    warning: Type[Warning]=Warning,
    exception: Type[Exception]=Exception,
    warning_levels: Optional[Union[Tuple[WarningsLevel, ...], Tuple[None]]]=None,
    exception_levels: Optional[Union[Tuple[WarningsLevel, ...], Tuple[None]]]=None
) -> None:
    """Warning or exception in validators."""
    if settings.warnings_level in (warning_levels or (WarningsLevel.Basic,)):
        warnings.warn(
            message + ' ' + auto_correct,
            warning,
            stacklevel=3
        )
    elif settings.warnings_level in (exception_levels or (WarningsLevel.Strict,)):
        raise exception(message)