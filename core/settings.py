from core.utils.enums import WarningsLevel
from core.utils.decorators import alternative
from core.utils.constants import Strings

class Settings:
    """ContextSettings."""

    __slots__ = ["__warnings_level"]

    __warnings_level: WarningsLevel

    @property
    def warnings_level(self) -> WarningsLevel:
        """Warnings level, which defines strictness of code flow."""
        return self.__warnings_level

    @warnings_level.setter
    def warnings_level(self, value: WarningsLevel) -> None:
        self.__warnings_level = value

    def __init__(self) -> None:
        self.__warnings_level = WarningsLevel.Strict

    @alternative(version=Strings.ANY_VERSION)
    def get_warnings_level(self) -> WarningsLevel:
        return self.__warnings_level
    
    @alternative(version=Strings.ANY_VERSION)
    def set_warnings_level(self, warnings_level: WarningsLevel=WarningsLevel.Strict) -> None:
        self.__warnings_level = warnings_level