"""type_aliases.py - Type aliases."""

from typing import (
    TypeAlias, Dict, Literal, TypedDict, List, Union, Any, Optional, NotRequired, Tuple, Callable
)

ConfigVersion: TypeAlias = Literal[1]
CommandClass: TypeAlias = Union[
    'WordCommandConfig', 'FallbackCommandConfig', 'FlagCommandConfig', 'OptionCommandConfig'
]
UnknownCommandClass: TypeAlias = Union[CommandClass, 'UnknownCommandConfig']
CommandType: TypeAlias = Literal["word", "fallback", "flag", "option"]
InternalCommandStates: TypeAlias = Literal["__base__", "__init__"]
CommandStates: TypeAlias = Dict[Union[InternalCommandStates, str], List[str]]
ConfigSupportedExtensions: TypeAlias = Literal[".json", ".json5"]
CommandPathSection: TypeAlias = Union[Literal["-any"], str]
CommandPathLevel: TypeAlias = Union[
    CommandPathSection, List[CommandPathSection], Tuple[CommandPathSection, ...]
]
CommandPath: TypeAlias = Union[List[CommandPathLevel], Tuple[CommandPathLevel, ...]]
CallableCommand: TypeAlias = Callable[[str, 'InputDict'], None]

class UnknownCommandConfig(TypedDict):
    """`CommandConfig` unknown variation for dynamic validations."""

    aliases: NotRequired[List[str]]
    type: NotRequired[CommandType]
    default: NotRequired[Any]
    children: NotRequired[Dict[str, CommandClass]]

class WordCommandConfig(TypedDict):
    """`Word` command type."""

    aliases: NotRequired[List[str]]
    type: Literal["word"]
    children: NotRequired[Dict[str, CommandClass]]

class FallbackCommandConfig(TypedDict):
    """`Fallback` command type."""

    type: Literal["fallback"]
    default: Any
    children: NotRequired[Dict[str, CommandClass]]

class FlagCommandConfig(TypedDict):
    """`Flag` command type."""

    aliases: NotRequired[List[str]]
    type: Literal["flag"]
    default: Optional[bool]

class OptionCommandConfig(TypedDict):
    """`Option` command type."""

    aliases: NotRequired[List[str]]
    type: Literal["option"]
    default: Any

class ConfigType(TypedDict):
    """Config typed dict."""

    version: ConfigVersion
    states: CommandStates
    commands: Dict[str, CommandClass]

class UnknownConfigType(TypedDict):
    """Unknown config type dict for dynamic validations."""

    version: NotRequired[ConfigVersion]
    states: NotRequired[CommandStates]
    commands: NotRequired[Dict[str, UnknownCommandClass]]

class InputDict(TypedDict):
    """Output dict for input."""

    path: List[str]
    flags: Dict[str, Optional[bool]]
    options: Dict[str, Any]

class CommandHistory(TypedDict):
    """Command history."""

    max_size: int
    """Max notes count. By default is `100`."""
    is_write_overflow: bool
    """Is delete the oldest notes from history and save the newest on max size limit. If disabled, new notes won't catched in history. By default is `True`."""
    notes: List[Tuple[str, InputDict]]
    """Catched inputs with tracking."""
