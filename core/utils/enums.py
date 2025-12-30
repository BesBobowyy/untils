from enum import IntEnum

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