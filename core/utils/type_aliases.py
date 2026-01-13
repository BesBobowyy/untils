from typing import TypeAlias, Dict, Literal, TypedDict, List, Union, Any, Optional, NotRequired, Tuple, Callable

ConfigVersion: TypeAlias = Literal[1]
CommandClass: TypeAlias = Union[
    'CommandConfig_Word', 'CommandConfig_Fallback', 'CommandConfig_Flag', 'CommandConfig_Option'
]
UnknownCommandClass: TypeAlias = Union[CommandClass, 'CommandConfig_Unknown']
CommandType: TypeAlias = Literal["word", "fallback", "flag", "option"]
InternalCommandStates: TypeAlias = Literal["__base__", "__init__"]
CommandStates: TypeAlias = Dict[Union[InternalCommandStates, str], List[str]]
ConfigSupportedExtensions: TypeAlias = Literal[".json", ".json5"]
CommandPath: TypeAlias = Union[
    List[Union[str, List[str], Tuple[str, ...]]],
    Tuple[Union[str, List[str], Tuple[str, ...]], ...]
]
CallableCommand: TypeAlias = Callable[[str, 'InputDict'], None]

class CommandConfig_Unknown(TypedDict):
    aliases: NotRequired[List[str]]
    type: NotRequired[CommandType]
    default: NotRequired[Any]
    children: NotRequired[Dict[str, CommandClass]]

class CommandConfig_Word(TypedDict):
    aliases: NotRequired[List[str]]
    type: Literal["word"]
    children: NotRequired[Dict[str, CommandClass]]

class CommandConfig_Fallback(TypedDict):
    type: Literal["fallback"]
    default: Any
    children: NotRequired[Dict[str, CommandClass]]

class CommandConfig_Flag(TypedDict):
    aliases: NotRequired[List[str]]
    type: Literal["flag"]
    default: Optional[bool]

class CommandConfig_Option(TypedDict):
    aliases: NotRequired[List[str]]
    type: Literal["option"]
    default: Any

class ConfigType(TypedDict):
    version: ConfigVersion
    states: CommandStates
    commands: Dict[str, CommandClass]

class UnknownConfigType(TypedDict):
    version: NotRequired[ConfigVersion]
    states: NotRequired[CommandStates]
    commands: NotRequired[Dict[str, UnknownCommandClass]]

class InputDict(TypedDict):
    path: List[str]
    flags: Dict[str, Optional[bool]]
    options: Dict[str, Any]