from core.utils.type_aliases import CommandType

from core.command import (
    CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode, CommandOptionNode, AliasNode
)

from typing import List, Any

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

        if node_type == "word":
            return CommandWordNode(name, node_type, aliases, children)
        elif node_type == "fallback":
            return CommandFallbackNode(name, node_type, default, children)
        elif node_type == "flag":
            return CommandFlagNode(name, node_type, aliases, default)
        elif node_type == "option":
            return CommandOptionNode(name, node_type, aliases, default)