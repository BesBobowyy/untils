"""`src/settings.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

import pytest

import src

@pytest.fixture
def settings() -> src.Settings:
    """Fixture for `pytest`."""

    return src.Settings()

def test_init(settings: src.Settings) -> None:
    """Tests `Settings` constructor."""

    assert settings.warnings_level == src.utils.WarningsLevel.STRICT
    assert settings.current_state == src.utils.InternalState.INIT.value

def test_warning(settings: src.Settings) -> None:
    """Tests `Settings.warning` method."""

    settings.warnings_level = src.utils.WarningsLevel.IGNORE

    #-- STAGE 1: Standard levels --#
    # WarningsLevel.IGNORE must be silent with errors.
    assert settings.warning(
        "WarningsLevel.IGNORE",
        '',
        src.utils.ConfigWarning,
        src.utils.ConfigError
    ) is None

    settings.warnings_level = src.utils.WarningsLevel.BASIC

    # WarningsLevel.BASIC must only warn about errors.
    pytest.warns(
        src.utils.ConfigWarning,
        lambda: settings.warning(
            "WarningsLevel.BASIC",
            '',
            src.utils.ConfigWarning,
            src.utils.ConfigError
        )
    )

    settings.warnings_level = src.utils.WarningsLevel.STRICT

    # WarningsLevel.STRICT must only warn about errors.
    pytest.raises(
        src.utils.ConfigError,
        lambda: settings.warning(
            "WarningsLevel.STRICT",
            '',
            src.utils.ConfigWarning,
            src.utils.ConfigError
        )
    )

    #-- STAGE 2: Custom levels --#
    settings.warnings_level = src.utils.WarningsLevel.STRICT

    assert settings.warning(
        "WarningsLevel.STRICT",
        '',
        src.utils.ConfigWarning,
        src.utils.ConfigError,
        warning_levels=(None,),
        exception_levels=(None,)
    ) is None

    settings.warnings_level = src.utils.WarningsLevel.BASIC

    pytest.raises(
        src.utils.ConfigError,
        lambda: settings.warning(
            "WarningsLevel.BASIC",
            '',
            src.utils.ConfigWarning,
            src.utils.ConfigError,
            warning_levels=(None,),
            exception_levels=(src.utils.WarningsLevel.BASIC, src.utils.WarningsLevel.STRICT)
        )
    )

def test_warnings_level_change(settings: src.Settings) -> None:
    """Tests warnings level change."""

    # WarningsLevel.STRICT
    assert settings.warnings_level == src.utils.WarningsLevel.STRICT

    # WarningsLevel.IGNORE
    settings.warnings_level = src.utils.WarningsLevel.IGNORE
    assert settings.warnings_level == src.utils.WarningsLevel.IGNORE

    # WarningsLevel.BASIC
    settings.warnings_level = src.utils.WarningsLevel.BASIC
    assert settings.warnings_level == src.utils.WarningsLevel.BASIC

    # WarningsLevel.STRICT
    settings.warnings_level = src.utils.WarningsLevel.STRICT
    assert settings.warnings_level == src.utils.WarningsLevel.STRICT

def test_current_state_change(settings: src.Settings) -> None:
    """Tests current state change."""

    # "__init__"
    settings.warnings_level = src.utils.WarningsLevel.STRICT
    assert settings.current_state == src.utils.InternalState.INIT.value

    # "__base__"
    with pytest.raises(ValueError) as e_info:    # pyright: ignore[reportUnusedVariable]
        settings.current_state = src.utils.InternalState.BASE.value
    assert settings.current_state == src.utils.InternalState.INIT.value
