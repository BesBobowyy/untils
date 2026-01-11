from enum import IntEnum, Enum

class LibraryVersionStatus(IntEnum):
    """The library version status: \"Development\", \"Alpha\", \"Beta\" or \"Release\"."""

    d = 0
    """Development."""
    a = 1
    """Alpha."""
    b = 2
    """Beta."""
    r = 3
    """Release."""

class WarningsLevel(IntEnum):
    """Error alerts level."""

    Ignore = 0
    """Silent errors."""
    Basic = 1
    """Display with auto-correcting."""
    Strict = 2
    """Raise exceptions."""

class ConfigVersions(IntEnum):
    """The all config versions."""

    V1 = 1

class RawTokenType(IntEnum):
    """The raw token type."""

    SPACE = 0
    WORD = 1
    MINUS = 2
    NOT = 3
    STRING = 4

    def __repr__(self) -> str:
        return self.name

class FinalTokenType(IntEnum):
    """The final token type."""

    WORD = 0
    FLAG = 1
    OPTION = 2

    def __repr__(self) -> str:
        return self.name

class InternalState(Enum):
    """The all internal states in config."""

    BASE = "__base__"
    """Commands in this state will be always available."""
    INIT = "__init__"
    """Initial state."""