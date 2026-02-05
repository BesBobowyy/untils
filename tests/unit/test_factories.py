"""`src/factories.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

from typing import List, Any

import pytest

import src

def test_command_node_factory() -> None:
    """Tests `CommandNodeFactory` class."""

    # `Word` node.
    name: str = "word_node"
    node_type: src.utils.CommandType = "word"
    aliases: List[src.AliasNode] = [src.AliasNode("word_node", "wn")]
    default: Any = None
    children: List[src.CommandNode] = []

    assert src.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Fallback` node.
    name: str = "fallback_node"
    node_type: src.utils.CommandType = "fallback"
    aliases: List[src.AliasNode] = [src.AliasNode("fallback_node", "fan")]
    default: Any = None
    children: List[src.CommandNode] = []

    assert src.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Flag` node.
    name: str = "flag_node"
    node_type: src.utils.CommandType = "flag"
    aliases: List[src.AliasNode] = [src.AliasNode("flag_node", "fln")]
    default: Any = None
    children: List[src.CommandNode] = []

    assert src.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Option` node.
    name: str = "option_node"
    node_type: src.utils.CommandType = "option"
    aliases: List[src.AliasNode] = [src.AliasNode("option_node", "on")]
    default: Any = None
    children: List[src.CommandNode] = []

    assert src.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None
