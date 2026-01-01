from core.utils.type_aliases import UnknownConfigType

from core.settings import Settings

from typing import Protocol, Any, runtime_checkable

@runtime_checkable
class IOReaderMixin(Protocol):
    """Protocol for all IOReader mixins."""

    @staticmethod
    def read(settings: Settings, file_path: str) -> UnknownConfigType: ...

class Factoric(Protocol):
    """Factory protocol."""

    @classmethod
    def create(cls, settings: Settings, *args: Any, **kwargs: Any) -> Any: ...