"""factories.py - All factories."""

# pylint: disable=too-few-public-methods

from typing import List, Any

from src.utils.type_aliases import CommandType

from src.command import (
    CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode, CommandOptionNode, AliasNode
)

class CommandNodeFactory:
    """Factory class for command nodes."""

    @classmethod
    def create(
        cls,
        name: str,
        node_type: CommandType,
        aliases: List[AliasNode],
        default: Any,
        children: List[CommandNode]
    ) -> CommandNode:
        """Creates a command node by a template.
        
        Args:
            name: The command name.
            node_type: The command type.
            aliases: The command aliases.
            default: The command default value.
            children: The nest commands.
        """

        return {
            "word": CommandWordNode(name, node_type, aliases, children),
            "fallback": CommandFallbackNode(name, node_type, default, children),
            "flag": CommandFlagNode(name, node_type, aliases, default),
            "option": CommandOptionNode(name, node_type, aliases, default)
        }[node_type]
