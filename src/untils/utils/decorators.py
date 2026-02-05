"""decorators.py - All decorators for functions and methods to define them status."""

import warnings

from functools import wraps

from typing import Callable, Any, TypeVar

from untils.utils.constants import Strings

T = TypeVar("T", bound=Callable[..., Any])

def deprecated(
    version: str = Strings.UNKNOWN_VERSION,
    reason: str = Strings.DEPRECATED_METHOD
) -> Callable[[T], T]:
    """Deprecated method decorator."""

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__}: {reason} [Version: {version}]",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper    # pyright: ignore[reportReturnType]
    return decorator

def alternative(
    version: str = Strings.UNKNOWN_VERSION,
    reason: str = Strings.ALTERNATIVE_METHOD
) -> Callable[[T], T]:
    """Alternative method decorator."""

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__}: {reason} [Version: {version}]",
                FutureWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper    # pyright: ignore[reportReturnType]
    return decorator
