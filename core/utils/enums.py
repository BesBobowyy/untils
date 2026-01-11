from enum import IntEnum, Enum

class WarningsLevel(IntEnum):
    """Controls, how much errors affect on code flow."""

    '''
    IgnoreErrors = 2**0    # No errors, auto-correcting.
    IgnoreWarnings = 2**1    # No warnings, auto-correcting.
    BasicErrors = 2**2    # Throws critical errros, but immaterial errors ignores.
    BasicWarnings = 2**3     # Displays critical warnings, but immaterial warnings ignores.
    StrictErrors = 2**4    # Throws any errors.
    StrictWarnings = 2**5    # Display all warnings.
    '''

    Ignore = 0    # No errors, auto-correcting.
    Basic = 1    # Critical errors.
    Strict = 2    # Any errors and warnings.

class ConfigVersions(IntEnum):
    """All config versions."""

    V1 = 1

class RawTokenType(IntEnum):
    """Raw token type."""

    SPACE = 0
    WORD = 1
    MINUS = 2
    NOT = 3
    STRING = 4

    def __repr__(self) -> str:
        return self.name

class FinalTokenType(IntEnum):
    """Final token type."""

    WORD = 0
    FLAG = 1
    OPTION = 2

    def __repr__(self) -> str:
        return self.name

class InternalState(Enum):
    """All internal states in config."""

    BASE = "__base__"
    INIT = "__init__"