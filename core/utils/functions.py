from core.utils.enums import WarningsLevel

from core.settings import Settings

import warnings

def warning(
    settings: Settings,
    message: str,
    auto_correct: str,
    warning: type[Warning],
    exception: type[Exception]
) -> None:
    """Warning or exception in validators."""
    if settings.warnings_level == WarningsLevel.Basic:
        warnings.warn(
            message + auto_correct,
            warning,
            stacklevel=2
        )
    elif settings.warnings_level == WarningsLevel.Strict:
        raise exception(message)