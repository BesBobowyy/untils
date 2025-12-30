from core.utils.type_aliases import ConfigVersion

from core.command import StateNode, CommandNode

from typing import List

from dataclasses import dataclass

@dataclass(frozen=True)
class CommandsConfig:
    """Immutable class for configs."""

    version: ConfigVersion
    states: List[StateNode]
    commands: List[CommandNode]
    
    def __str__(self) -> str:
        return f"CommandsConfig(version={self.version}, states={self.states}, commands={self.commands})"