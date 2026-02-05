"""`src/input_token.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

import pytest

import src

def test_raw_input_token() -> None:
    """Tests `RawInputToken`."""

    for token_type in src.utils.RawTokenType:
        raw_input_token: src.RawInputToken = src.RawInputToken(token_type, token_type.name)
        assert raw_input_token.type == token_type
        assert raw_input_token.value == token_type.name

def test_word_input_token() -> None:
    """Tests `FinalInputTokenWord`."""

    word_input_token: src.FinalInputTokenWord = src.FinalInputTokenWord("word_token")
    assert word_input_token.type == src.utils.FinalTokenType.WORD
    assert word_input_token.value == "word_token"

def test_flag_input_token() -> None:
    """Tests `FinalInputTokenFlag`."""

    word_input_token: src.FinalInputTokenFlag = src.FinalInputTokenFlag("flag_token", True)
    assert word_input_token.type == src.utils.FinalTokenType.FLAG
    assert word_input_token.name == "flag_token"
    assert word_input_token.value

def test_option_input_token() -> None:
    """Tests `FinalInputTokenOption`."""

    word_input_token: src.FinalInputTokenOption = src.FinalInputTokenOption("option_token", "42")
    assert word_input_token.type == src.utils.FinalTokenType.OPTION
    assert word_input_token.name == "option_token"
    assert word_input_token.value == "42"
