"""`src/settings.py` tests."""

# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=redefined-outer-name

import pytest

import untils

@pytest.fixture
def settings() -> untils.Settings:
    """Fixture for `pytest`."""

    return untils.Settings()

def test_init(settings: untils.Settings) -> None:
    """Tests `Settings` constructor."""

    assert settings.warnings_level == untils.utils.WarningsLevel.STRICT
    assert settings.current_state == untils.utils.InternalState.INIT.value

def test_warning(settings: untils.Settings) -> None:
    """Tests `Settings.warning` method."""

    settings.warnings_level = untils.utils.WarningsLevel.IGNORE

    #-- STAGE 1: Standard levels --#
    # WarningsLevel.IGNORE must be silent with errors.
    assert settings.warning(
        "WarningsLevel.IGNORE",
        '',
        untils.utils.ConfigWarning,
        untils.utils.ConfigError
    ) is None

    settings.warnings_level = untils.utils.WarningsLevel.BASIC

    # WarningsLevel.BASIC must only warn about errors.
    pytest.warns(
        untils.utils.ConfigWarning,
        lambda: settings.warning(
            "WarningsLevel.BASIC",
            '',
            untils.utils.ConfigWarning,
            untils.utils.ConfigError
        )
    )

    settings.warnings_level = untils.utils.WarningsLevel.STRICT

    # WarningsLevel.STRICT must only warn about errors.
    pytest.raises(
        untils.utils.ConfigError,
        lambda: settings.warning(
            "WarningsLevel.STRICT",
            '',
            untils.utils.ConfigWarning,
            untils.utils.ConfigError
        )
    )

    #-- STAGE 2: Custom levels --#
    settings.warnings_level = untils.utils.WarningsLevel.STRICT

    assert settings.warning(
        "WarningsLevel.STRICT",
        '',
        untils.utils.ConfigWarning,
        untils.utils.ConfigError,
        warning_levels=(None,),
        exception_levels=(None,)
    ) is None

    settings.warnings_level = untils.utils.WarningsLevel.BASIC

    pytest.raises(
        untils.utils.ConfigError,
        lambda: settings.warning(
            "WarningsLevel.BASIC",
            '',
            untils.utils.ConfigWarning,
            untils.utils.ConfigError,
            warning_levels=(None,),
            exception_levels=(untils.utils.WarningsLevel.BASIC, untils.utils.WarningsLevel.STRICT)
        )
    )

def test_warnings_level_change(settings: untils.Settings) -> None:
    """Tests warnings level change."""

    # WarningsLevel.STRICT
    assert settings.warnings_level == untils.utils.WarningsLevel.STRICT

    # WarningsLevel.IGNORE
    settings.warnings_level = untils.utils.WarningsLevel.IGNORE
    assert settings.warnings_level == untils.utils.WarningsLevel.IGNORE

    # WarningsLevel.BASIC
    settings.warnings_level = untils.utils.WarningsLevel.BASIC
    assert settings.warnings_level == untils.utils.WarningsLevel.BASIC

    # WarningsLevel.STRICT
    settings.warnings_level = untils.utils.WarningsLevel.STRICT
    assert settings.warnings_level == untils.utils.WarningsLevel.STRICT

def test_current_state_change(settings: untils.Settings) -> None:
    """Tests current state change."""

    # "__init__"
    settings.warnings_level = untils.utils.WarningsLevel.STRICT
    assert settings.current_state == untils.utils.InternalState.INIT.value

    # "__base__"
    with pytest.raises(ValueError) as e_info:    # pyright: ignore[reportUnusedVariable]
        settings.current_state = untils.utils.InternalState.BASE.value
    assert settings.current_state == untils.utils.InternalState.INIT.value
