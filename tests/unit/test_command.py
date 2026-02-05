"""`src/command.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

from typing import Tuple

import pytest

import untils

def test_command_node() -> None:
    """Tests `CommandNode`."""

    #-- STAGE 1: Construnctors --#
    word_command_node: untils.CommandWordNode = untils.CommandWordNode(
        "word_command_node",
        "word",
        [untils.AliasNode("word", "w")],
        []
    )
    assert word_command_node.name == "word_command_node"
    assert word_command_node.type == "word"
    assert word_command_node.aliases == [untils.AliasNode("word", "w")]
    assert not word_command_node.children

    fallback_command_node: untils.CommandFallbackNode = untils.CommandFallbackNode(
        "fallback_command_node",
        "fallback",
        "null",
        []
    )
    assert fallback_command_node.name == "fallback_command_node"
    assert fallback_command_node.type == "fallback"
    assert fallback_command_node.default == "null"
    assert not fallback_command_node.children

    flag_command_node: untils.CommandFlagNode = untils.CommandFlagNode(
        "flag_command_node",
        "flag",
        [untils.AliasNode("flag", "f")],
        None
    )
    assert flag_command_node.name == "flag_command_node"
    assert flag_command_node.type == "flag"
    assert flag_command_node.aliases == [untils.AliasNode("flag", "f")]
    assert flag_command_node.default is None

    option_command_node: untils.CommandOptionNode = untils.CommandOptionNode(
        "option_command_node",
        "option",
        [untils.AliasNode("option", "o")],
        None
    )
    assert option_command_node.name == "option_command_node"
    assert option_command_node.type == "option"
    assert option_command_node.aliases == [untils.AliasNode("option", "o")]
    assert option_command_node.default is None

    #-- STAGE 2: Equals --#
    nodes: Tuple[untils.CommandNode, ...] = (
        word_command_node,
        fallback_command_node,
        flag_command_node,
        option_command_node
    )

    for first_node in nodes:
        for second_node in nodes:
            if id(first_node) != id(second_node):
                assert first_node != second_node
            else:
                assert first_node == second_node

    #-- STAGE 3: Alias equals --#
    for i, node in enumerate(nodes):
        if node.type == "fallback":
            # `Fallback` nodes hasn't aliases.
            continue

        correct_alias: untils.AliasNode = untils.AliasNode(node.name, str(i))
        incorrect_alias: untils.AliasNode = untils.AliasNode(node.name+"_alias", str(i))

        assert correct_alias == node
        assert incorrect_alias != node

    # `Fallback` aliases are always incorrect.
    fallback_alias: untils.AliasNode = untils.AliasNode(fallback_command_node.name, "fnode")
    assert fallback_alias != fallback_command_node
