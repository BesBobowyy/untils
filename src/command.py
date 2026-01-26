from src.utils.type_aliases import CommandType

from typing import List, Any

from dataclasses import dataclass

@dataclass(frozen=True)
class AliasNode():
    """Command alias name container."""

    original_name: str
    """Original command name."""
    alias_name: str
    """Alias name."""

    def __str__(self) -> str:
        return f"AliasNode('{self.original_name}' -> '{self.alias_name}')"

@dataclass(frozen=True)
class CommandNode:
    """Universal template for command nodes."""

    name: str
    """Command name."""
    type: CommandType
    """Command type."""

    def __eq__(self, value: object) -> bool:
        if isinstance(value, CommandNode):
            return self.name == value.name and self.type == value.type
        return False

@dataclass(frozen=True)
class CommandWordNode(CommandNode):
    """The word command type."""

    aliases: List[AliasNode]
    """Command aliases."""
    children: List[CommandNode]
    """Next commands below this."""

    def __str__(self) -> str:
        return f"CommandWordNode[{self.name} : {self.aliases}]{self.children}"

@dataclass(frozen=True)
class CommandFallbackNode(CommandNode):
    """Command node for fallback type."""

    default: str
    """A default value."""
    children: List[CommandNode]
    """Next commands below this."""

    def __str__(self) -> str:
        return f"CommandFallbackNode[{self.name}](default='{self.default}'){self.children}"

@dataclass(frozen=True)
class CommandFlagNode(CommandNode):
    """Command node for flag type."""

    aliases: List[AliasNode]
    """Command aliases."""
    default: Any
    """A default value."""
    
    def __str__(self) -> str:
        return f"CommandFlagNode[{self.name} : {self.aliases}](default={repr(self.default)})"

@dataclass(frozen=True)
class CommandOptionNode(CommandNode):
    """Command node for option type."""

    aliases: List[AliasNode]
    """Command aliases."""
    default: Any
    """A default value."""

    def __str__(self) -> str:
        return f"CommandOptionNode[{self.name} : {self.aliases}](default={repr(self.default)})"

@dataclass(frozen=True)
class StateNode:
    """A state node in config."""

    name: str
    """The state name."""
    is_internal: bool
    """Is internal state, which typed in the format `__{name}__`."""
    commands: List[str]
    """Allowed commands by this state."""

    def __str__(self) -> str:
        return f"StateNode[{'!' if self.is_internal else ''}{self.name}]{self.commands}"