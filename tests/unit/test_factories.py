"""`src/factories.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

from typing import List, Any

import pytest

import untils

def test_command_node_factory() -> None:
    """Tests `CommandNodeFactory` class."""

    # `Word` node.
    name: str = "word_node"
    node_type: untils.utils.CommandType = "word"
    aliases: List[untils.AliasNode] = [untils.AliasNode("word_node", "wn")]
    default: Any = None
    children: List[untils.CommandNode] = []

    assert untils.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Fallback` node.
    name: str = "fallback_node"
    node_type: untils.utils.CommandType = "fallback"
    aliases: List[untils.AliasNode] = [untils.AliasNode("fallback_node", "fan")]
    default: Any = None
    children: List[untils.CommandNode] = []

    assert untils.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Flag` node.
    name: str = "flag_node"
    node_type: untils.utils.CommandType = "flag"
    aliases: List[untils.AliasNode] = [untils.AliasNode("flag_node", "fln")]
    default: Any = None
    children: List[untils.CommandNode] = []

    assert untils.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None

    # `Option` node.
    name: str = "option_node"
    node_type: untils.utils.CommandType = "option"
    aliases: List[untils.AliasNode] = [untils.AliasNode("option_node", "on")]
    default: Any = None
    children: List[untils.CommandNode] = []

    assert untils.CommandNodeFactory.create(
        name, node_type, aliases, default, children
    ) is not None
