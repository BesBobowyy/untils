from core.utils.type_aliases import UnknownConfigType
from core.utils.enums import FinalTokenType

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

class FinalInputProtocol(Protocol):
    """Final input token protocol."""

    type: FinalTokenType
    value: Any