from core.utils.enums import WarningsLevel

from core.settings import Settings

from typing import Type, Optional, Tuple

import warnings

def warning(
    settings: Settings,
    message: str,
    auto_correct: str,
    warning: Type[Warning]=Warning,
    exception: Type[Exception]=Exception,
    warning_levels: Optional[Tuple[WarningsLevel]]=None,
    exception_levels: Optional[Tuple[WarningsLevel]]=None
) -> None:
    """Warning or exception in validators."""
    if settings.warnings_level in (warning_levels or ()):
        warnings.warn(
            message + auto_correct,
            warning,
            stacklevel=2
        )
    elif settings.warnings_level in (exception_levels or ()):
        raise exception(message)