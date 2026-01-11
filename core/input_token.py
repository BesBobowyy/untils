from core.utils.enums import RawTokenType, FinalTokenType

from typing import Any, Literal

from dataclasses import dataclass

@dataclass(frozen=True)
class RawInputToken:
    """Raw input token for Tokenizer."""

    type: RawTokenType
    value: str

    def __repr__(self) -> str:
        return f"RawInputToken[{self.type.name}](value='{self.value}')"



class FinalInputTokenWord:
    """Word type of FinalInputToken."""

    type: Literal[FinalTokenType.WORD]
    value: str

    def __init__(self, value: str) -> None:
        self.type = FinalTokenType.WORD
        self.value = value
    
    def __repr__(self) -> str:
        return f"FinalInputTokenWord(value={self.value})"

class FinalInputTokenFlag:
    """Flag type of FinalInputToken."""

    type: Literal[FinalTokenType.FLAG]
    name: str
    value: bool

    def __init__(self, name: str, value: bool) -> None:
        self.type = FinalTokenType.FLAG
        self.name = name
        self.value = value
    
    def __repr__(self) -> str:
        return f"FinalInputTokenFlag(name={self.name}, value={self.value})"

class FinalInputTokenOption:
    """Option type of FinalInputToken."""

    type: Literal[FinalTokenType.OPTION]
    name: str
    value: Any

    def __init__(self, name: str, value: Any) -> None:
        self.type = FinalTokenType.OPTION
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"FinalInputTokenOption(name={self.name}, value={self.value})"