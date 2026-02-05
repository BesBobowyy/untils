"""protocols.py - Abstract and Protocol classes."""

# pyright: reportReturnType=false

# pylint: disable=too-few-public-methods

from typing import Protocol, Any, runtime_checkable
from abc import ABC, abstractmethod

from untils.utils.type_aliases import UnknownConfigType
from untils.utils.enums import FinalTokenType

from untils.settings import Settings

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
    def read(settings: Settings, file_path: str) -> UnknownConfigType:
        """Mixin for `IOReader`."""

class Factoric(Protocol):
    """The protocol for all factories."""

    @classmethod
    def create(cls, settings: Settings, *args: Any, **kwargs: Any) -> Any:
        """Creates an object."""

class FinalInputProtocol(Protocol):
    """The protocol for all final input tokens."""

    type: FinalTokenType
    value: Any
