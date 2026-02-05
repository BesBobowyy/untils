"""input_token.py - Raw and Final input tokens for `Tokenizer` and `InputValidator`."""

# pylint: disable=too-few-public-methods

from typing import Any, Literal

from dataclasses import dataclass

from untils.utils.enums import RawTokenType, FinalTokenType

@dataclass(frozen=True)
class RawInputToken:
    """The raw input token for `Tokenizer`."""

    type: RawTokenType
    """The raw command type."""
    value: str
    """The raw value."""

    def __repr__(self) -> str:
        return f"RawInputToken[{self.type.name}](value='{self.value}')"



class FinalInputTokenWord:
    """The word type of `FinalInputToken`."""

    type: Literal[FinalTokenType.WORD]
    """The command type. Is literal."""
    value: str
    """The command value."""

    def __init__(self, value: str) -> None:
        self.type = FinalTokenType.WORD
        self.value = value

    def __repr__(self) -> str:
        return f"FinalInputTokenWord(value={self.value})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenWord):
            return self.value == value.value
        return False

    def __ne__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenWord):
            return self.value != value.value
        return True

class FinalInputTokenFlag:
    """The flag type of `FinalInputToken`."""

    type: Literal[FinalTokenType.FLAG]
    """The command type. Is literal."""
    name: str
    """The command name."""
    value: bool
    """The command value."""

    def __init__(self, name: str, value: bool) -> None:
        self.type = FinalTokenType.FLAG
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"FinalInputTokenFlag(name={self.name}, value={self.value})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenFlag):
            return self.name == value.name and self.value == value.value
        return False

    def __ne__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenFlag):
            return self.name != value.name or self.value != value.value
        return True

class FinalInputTokenOption:
    """The option type of `FinalInputToken`."""

    type: Literal[FinalTokenType.OPTION]
    """The command type. Is literal."""
    name: str
    """The command name."""
    value: Any
    """The command value."""

    def __init__(self, name: str, value: Any) -> None:
        self.type = FinalTokenType.OPTION
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"FinalInputTokenOption(name={self.name}, value={self.value})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenOption):
            return self.name == value.name and self.value == value.value
        return False

    def __ne__(self, value: object) -> bool:
        if isinstance(value, FinalInputTokenOption):
            return self.name != value.name or self.value != value.value
        return True
