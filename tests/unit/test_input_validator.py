"""`src/input_token.py` tests."""

# pyright: reportUnusedImport=false
# pyright: reportPrivateUsage=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import functools

from typing import Tuple, TypeAlias

import pytest

import src

Objects: TypeAlias = Tuple[src.Settings, src.CommandsConfig, src.InputValidator]

@pytest.fixture
def objects() -> Objects:
    """Fixture for `pytest`."""

    settings: src.Settings = src.Settings()
    config: src.CommandsConfig = src.CommandsConfig(1, [], [])
    input_validator: src.InputValidator = src.InputValidator(settings, config, [])
    return (settings, config, input_validator)

def test_init(objects: Objects) -> None:
    """Tests `InputValidator` constructor."""

    settings, config, input_validator = objects

    assert input_validator._settings == settings
    assert input_validator._config == config
    assert not input_validator._input_tokens
    assert not input_validator._result
    assert input_validator._i == 0

def test_warning_out_of_bounce(objects: Objects) -> None:
    """Tests `InputValidator.warning_out_of_bounce` method."""

    settings, _, input_validator = objects

    settings.warnings_level = src.utils.WarningsLevel.BASIC
    pytest.warns(src.utils.InputStructureWarning, input_validator.warning_out_of_bounce)

    settings.warnings_level = src.utils.WarningsLevel.STRICT
    pytest.raises(src.utils.InputStructureError, input_validator.warning_out_of_bounce)

def test_expect_end(objects: Objects) -> None:
    """Tests `InputValidator.expect_end` method."""

    settings, _, input_validator = objects

    input_validator._input_tokens = [src.RawInputToken(src.utils.RawTokenType.WORD, "test")]

    for i in range(-2, 3):
        for level in (src.utils.WarningsLevel.BASIC, src.utils.WarningsLevel.STRICT):
            settings.warnings_level = level

            expected_warning = src.utils.InputValuesWarning if i <= 0 else src.utils.InputStructureWarning
            expected_exception = src.utils.InputValuesError if i <= 0 else src.utils.InputStructureError

            if level == src.utils.WarningsLevel.BASIC:
                pytest.warns(expected_warning, functools.partial(input_validator.expect_end, i))
            elif level == src.utils.WarningsLevel.STRICT:
                pytest.raises(expected_exception, functools.partial(input_validator.expect_end, i))

def test_validation_by_parts(objects: Objects) -> None:
    """Tests `InputValidator` validation methods."""

    settings, config, _ = objects

    # `Word` token.
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.WORD, "word")
        ]
    )

    input_validator.validate_token_word()
    assert input_validator._result == [src.FinalInputTokenWord("word")]
    assert input_validator._i == 1

    # `Flag` token.
    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.WORD, "T")
        ]
    )

    input_validator.validate_token_flag()
    assert input_validator._result == [src.FinalInputTokenFlag("T", True)]
    assert input_validator._i == 0

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.NOT, "!"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "T")
        ]
    )

    input_validator.validate_token_flag()
    assert input_validator._result == [src.FinalInputTokenFlag("T", False)]
    assert input_validator._i == 1

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.NOT, "!"),
            src.RawInputToken(src.utils.RawTokenType.NOT, "!"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(src.utils.InputStructureError, input_validator.validate_token_flag)

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.NOT, "!"),
            src.RawInputToken(src.utils.RawTokenType.MINUS, "-"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(src.utils.InputStructureError, input_validator.validate_token_flag)

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.NOT, "!"),
            src.RawInputToken(src.utils.RawTokenType.SPACE, " "),
            src.RawInputToken(src.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(src.utils.InputStructureError, input_validator.validate_token_flag)

    # `Option` token.
    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.WORD, "name"),
            src.RawInputToken(src.utils.RawTokenType.SPACE, ' '),
            src.RawInputToken(src.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [src.FinalInputTokenOption("name", "value")]
    assert input_validator._i == 2

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.WORD, "option"),
            src.RawInputToken(src.utils.RawTokenType.MINUS, "-"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "name"),
            src.RawInputToken(src.utils.RawTokenType.SPACE, ' '),
            src.RawInputToken(src.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [src.FinalInputTokenOption("option-name", "value")]
    assert input_validator._i == 4

    del input_validator
    input_validator: src.InputValidator = src.InputValidator(
        settings,
        config,
        [
            src.RawInputToken(src.utils.RawTokenType.WORD, "option"),
            src.RawInputToken(src.utils.RawTokenType.MINUS, "-"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "name"),
            src.RawInputToken(src.utils.RawTokenType.SPACE, ' '),
            src.RawInputToken(src.utils.RawTokenType.WORD, "option"),
            src.RawInputToken(src.utils.RawTokenType.MINUS, "-"),
            src.RawInputToken(src.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [src.FinalInputTokenOption("option-name", "option-value")]
    assert input_validator._i == 7

    # TODO: Finish test.
