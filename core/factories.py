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
        if node_type == "word":
            return CommandWordNode(name, node_type, aliases, children)
        elif node_type == "fallback":
            return CommandFallbackNode(name, node_type, default, children)
        elif node_type == "flag":
            return CommandFlagNode(name, node_type, aliases, default)
        elif node_type == "option":
            return CommandOptionNode(name, node_type, aliases, default)