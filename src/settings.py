"""settings.py - Global context settings for much part of all library."""

# pyright: reportUnnecessaryIsInstance=false

from typing import Union

import logging

from src.utils.enums import WarningsLevel, InternalState
from src.utils.decorators import alternative
from src.utils.constants import Strings

class Settings:
    """The global context settings."""

    __slots__ = ["__warnings_level", "__current_state", "__logger"]

    __warnings_level: WarningsLevel
    __current_state: str
    __logger: logging.Logger

    @property
    def warnings_level(self) -> WarningsLevel:
        """Warnings level, which defines strictness of code flow."""
        return self.__warnings_level

    @warnings_level.setter
    def warnings_level(self, value: WarningsLevel) -> None:
        self.__warnings_level = value

    @property
    def current_state(self) -> str:
        """Current commands state."""
        return self.__current_state

    @current_state.setter
    def current_state(self, value: Union[str, InternalState]) -> None:
        if isinstance(value, str):
            self.__current_state = value
        elif isinstance(value, InternalState):
            self.__current_state = value.value

    @property
    def logger(self) -> logging.Logger:
        """Returns settings logger."""
        return self.__logger

    def __init__(self) -> None:
        self.__warnings_level = WarningsLevel.STRICT
        self.__current_state = InternalState.INIT.value
        self.__logger = logging.getLogger(__name__)
        self.__logger.debug(Strings.LOG_SETTINGS_INIT)

    @alternative(version=Strings.ANY_VERSION)
    def get_warnings_level(self) -> WarningsLevel:
        """[!ALT] Get a warnings level.\n
        <This method is alternative for the standart. In real product use the property `Settings.warnings_level`.>
        
        Returns:
            The current warnings level.
        """

        return self.__warnings_level

    @alternative(version=Strings.ANY_VERSION)
    def set_warnings_level(self, warnings_level: WarningsLevel=WarningsLevel.STRICT) -> None:
        """[!ALT] Sets a warnings level.\n
        <This method is alternative for the standart. In real product use the property `Settings.warnings_level`.>
        
        Args:
            warnings_level: The warnings level.
        """

        self.__warnings_level = warnings_level
