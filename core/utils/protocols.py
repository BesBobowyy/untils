from core.utils.type_aliases import UnknownConfigType
from core.utils.enums import FinalTokenType

from core.settings import Settings

from typing import Protocol, Any, runtime_checkable
from abc import ABC, abstractmethod

class IOReaderMixin(ABC):
    """The abstract class for all IOReader mixins."""

    @staticmethod
    @abstractmethod
    def read(settings: Settings, file_path: str) -> UnknownConfigType:
        """Reads a config file."""

@runtime_checkable
class IOReaderProtocol(Protocol):
    """The protocol for all IOReader mixins."""

    @staticmethod
    def read(settings: Settings, file_path: str) -> UnknownConfigType: ...

class Factoric(Protocol):
    """The protocol for all factories."""

    @classmethod
    def create(cls, settings: Settings, *args: Any, **kwargs: Any) -> Any: ...

class FinalInputProtocol(Protocol):
    """The protocol for all final input tokens."""

    type: FinalTokenType
    value: Any