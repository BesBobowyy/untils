from core.utils.type_aliases import CommandType

from typing import List, Any

from dataclasses import dataclass

@dataclass(frozen=True)
class AliasNode():
    """Alias node for another naming of commands."""

    original_name: str
    alias_name: str

    def __str__(self) -> str:
        return f"AliasNode('{self.original_name}' -> '{self.alias_name}')"

@dataclass(frozen=True)
class CommandNode:
    """Command node in command hierarchy."""

    name: str
    type: CommandType

    def __eq__(self, value: object) -> bool:
        if isinstance(value, CommandNode):
            return self.name == value.name and self.type == value.type
        return False

@dataclass(frozen=True)
class CommandWordNode(CommandNode):
    """Command node for word type."""

    aliases: List['AliasNode']
    children: List[CommandNode]

    def __str__(self) -> str:
        return f"CommandWordNode[{self.name} : {self.aliases}]{self.children}"

@dataclass(frozen=True)
class CommandFallbackNode(CommandNode):
    """Command node for fallback type."""

    default: Any
    children: List[CommandNode]

    def __str__(self) -> str:
        return f"CommandFallbackNode[{self.name}](default={repr(self.default)}){self.children}"

@dataclass(frozen=True)
class CommandFlagNode(CommandNode):
    """Command node for flag type."""

    aliases: List['AliasNode']
    default: Any
    
    def __str__(self) -> str:
        return f"CommandFlagNode[{self.name} : {self.aliases}](default={repr(self.default)})"

@dataclass(frozen=True)
class CommandOptionNode(CommandNode):
    """Command node for option type."""

    aliases: List['AliasNode']
    default: Any

    def __str__(self) -> str:
        return f"CommandOptionNode[{self.name} : {self.aliases}](default={repr(self.default)})"

@dataclass(frozen=True)
class StateNode:
    """State node for states."""

    name: str
    is_internal: bool
    commands: List[str]

    def __str__(self) -> str:
        return f"StateNode[{'!' if self.is_internal else ''}{self.name}]{self.commands}"