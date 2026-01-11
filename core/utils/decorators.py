from core.utils.constants import Strings

from functools import wraps

from typing import Callable, Any, TypeVar
FuncType = TypeVar("FuncType", bound=Callable[..., Any])

import warnings

def deprecated(
    version: str = Strings.UNKNOWN_VERSION,
    reason: str = Strings.DEPRECATED_METHOD
) -> Callable[[FuncType], FuncType]:
    """Deprecated method decorator."""

    def decorator(func: FuncType) -> FuncType:
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
) -> Callable[[FuncType], FuncType]:
    """Alternative method decorator."""

    def decorator(func: FuncType) -> FuncType:
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