"""commands_config.py - Commands config."""

from typing import List

from dataclasses import dataclass

from src.utils.type_aliases import ConfigVersion

from src.command import StateNode, CommandNode

@dataclass(frozen=True)
class CommandsConfig:
    """Configuration class."""

    version: ConfigVersion
    """The configuration version. All supported versions are defined in `ConfigVersions`. The latest version is defined in `Constants.LATEST_CONFIG_VERSION`."""
    states: List[StateNode]
    """All written states. Use states for context separation."""
    commands: List[CommandNode]
    """All available commands for user."""

    def __str__(self) -> str:
        return f"CommandsConfig(version={self.version}, states={self.states}, commands={self.commands})"
