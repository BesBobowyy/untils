from core.utils.enums import WarningsLevel, InternalState
from core.utils.decorators import alternative
from core.utils.constants import Strings

from typing import Union

class Settings:
    """ContextSettings."""

    __slots__ = ["__warnings_level", "__current_state"]

    __warnings_level: WarningsLevel
    __current_state: str

    @property
    def warnings_level(self) -> WarningsLevel:
        """Warnings level, which defines strictness of code flow."""
        return self.__warnings_level

    @warnings_level.setter
    def warnings_level(self, value: WarningsLevel) -> None:
        self.__warnings_level = value
    
    @property
    def current_state(self) -> str:
        """Current commands context state."""
        return self.__current_state

    @current_state.setter
    def current_state(self, value: Union[str, InternalState]) -> None:
        if type(value) == str:
            self.__current_state = value
        elif type(value) == InternalState:
            self.__current_state = value.value

    def __init__(self) -> None:
        self.__warnings_level = WarningsLevel.Strict
        self.current_state = InternalState.INIT.value

    @alternative(version=Strings.ANY_VERSION)
    def get_warnings_level(self) -> WarningsLevel:
        return self.__warnings_level
    
    @alternative(version=Strings.ANY_VERSION)
    def set_warnings_level(self, warnings_level: WarningsLevel=WarningsLevel.Strict) -> None:
        self.__warnings_level = warnings_level