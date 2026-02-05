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

import untils

Objects: TypeAlias = Tuple[untils.Settings, untils.CommandsConfig, untils.InputValidator]

@pytest.fixture
def objects() -> Objects:
    """Fixture for `pytest`."""

    settings: untils.Settings = untils.Settings()
    config: untils.CommandsConfig = untils.CommandsConfig(1, [], [])
    input_validator: untils.InputValidator = untils.InputValidator(settings, config, [])
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

    settings.warnings_level = untils.utils.WarningsLevel.BASIC
    pytest.warns(untils.utils.InputStructureWarning, input_validator.warning_out_of_bounce)

    settings.warnings_level = untils.utils.WarningsLevel.STRICT
    pytest.raises(untils.utils.InputStructureError, input_validator.warning_out_of_bounce)

def test_expect_end(objects: Objects) -> None:
    """Tests `InputValidator.expect_end` method."""

    settings, _, input_validator = objects

    input_validator._input_tokens = [untils.RawInputToken(untils.utils.RawTokenType.WORD, "test")]

    for i in range(-2, 3):
        for level in (untils.utils.WarningsLevel.BASIC, untils.utils.WarningsLevel.STRICT):
            settings.warnings_level = level

            expected_warning = untils.utils.InputValuesWarning if i <= 0 else untils.utils.InputStructureWarning
            expected_exception = untils.utils.InputValuesError if i <= 0 else untils.utils.InputStructureError

            if level == untils.utils.WarningsLevel.BASIC:
                pytest.warns(expected_warning, functools.partial(input_validator.expect_end, i))
            elif level == untils.utils.WarningsLevel.STRICT:
                pytest.raises(expected_exception, functools.partial(input_validator.expect_end, i))

def test_validation_by_parts(objects: Objects) -> None:
    """Tests `InputValidator` validation methods."""

    settings, config, _ = objects

    # `Word` token.
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "word")
        ]
    )

    input_validator.validate_token_word()
    assert input_validator._result == [untils.FinalInputTokenWord("word")]
    assert input_validator._i == 1

    # `Flag` token.
    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "T")
        ]
    )

    input_validator.validate_token_flag()
    assert input_validator._result == [untils.FinalInputTokenFlag("T", True)]
    assert input_validator._i == 0

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.NOT, "!"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "T")
        ]
    )

    input_validator.validate_token_flag()
    assert input_validator._result == [untils.FinalInputTokenFlag("T", False)]
    assert input_validator._i == 1

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.NOT, "!"),
            untils.RawInputToken(untils.utils.RawTokenType.NOT, "!"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(untils.utils.InputStructureError, input_validator.validate_token_flag)

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.NOT, "!"),
            untils.RawInputToken(untils.utils.RawTokenType.MINUS, "-"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(untils.utils.InputStructureError, input_validator.validate_token_flag)

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.NOT, "!"),
            untils.RawInputToken(untils.utils.RawTokenType.SPACE, " "),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "T")
        ]
    )

    pytest.raises(untils.utils.InputStructureError, input_validator.validate_token_flag)

    # `Option` token.
    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "name"),
            untils.RawInputToken(untils.utils.RawTokenType.SPACE, ' '),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [untils.FinalInputTokenOption("name", "value")]
    assert input_validator._i == 2

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "option"),
            untils.RawInputToken(untils.utils.RawTokenType.MINUS, "-"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "name"),
            untils.RawInputToken(untils.utils.RawTokenType.SPACE, ' '),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [untils.FinalInputTokenOption("option-name", "value")]
    assert input_validator._i == 4

    del input_validator
    input_validator: untils.InputValidator = untils.InputValidator(
        settings,
        config,
        [
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "option"),
            untils.RawInputToken(untils.utils.RawTokenType.MINUS, "-"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "name"),
            untils.RawInputToken(untils.utils.RawTokenType.SPACE, ' '),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "option"),
            untils.RawInputToken(untils.utils.RawTokenType.MINUS, "-"),
            untils.RawInputToken(untils.utils.RawTokenType.WORD, "value")
        ]
    )

    input_validator.validate_token_option()
    assert input_validator._result == [untils.FinalInputTokenOption("option-name", "option-value")]
    assert input_validator._i == 7

    # TODO: Finish test.
