'''
import sys

if sys.version_info >= (3, 13):
    # Python 3.13+
    from warnings import deprecated as builtin_deprecated

    def deprecated(version: str = '<unknown>', reason: str = "Deprecated Method") -> Callable[..., Any]:
        decorator = builtin_deprecated
        decorator.message = f"{reason} [Version: {version}]"    # pyright: ignore[reportAttributeAccessIssue]
        return decorator
else:
    # Python -3.12.X
    from functools import wraps
    import warnings

    def deprecated(version: str = '<unknown>', reason: str = "Deprecated Method") -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                warnings.warn(
                    f"{func.__name__}: {reason} [Version: {version}]",
                    DeprecationWarning,
                    stacklevel=2
                )
                return func(*args, **kwargs)
            return wrapper
        return decorator'''

from functools import wraps

from typing import Callable, Any

import warnings

def deprecated(version: str = '<unknown>', reason: str = "Deprecated Method") -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__}: {reason} [Version: {version}]",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator