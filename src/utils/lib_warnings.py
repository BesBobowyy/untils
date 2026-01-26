class ConfigWarning(Warning):
    """Warning class for all config validation issues."""

class FileWarning(ConfigWarning):
    """Warning class for IOReader issues."""

class ConfigStructureWarning(ConfigWarning):
    """Warning class for config structure issues."""

class ConfigValuesWarning(ConfigWarning):
    """Warning class for config values issues."""

class InputWarning(Warning):
    """Warning class for all input validation issues."""

class InputStructureWarning(InputWarning):
    """Warning class for input structure issues."""

class InputValuesWarning(InputWarning):
    """Warning class for input values issues."""

class ConfigError(Exception):
    """Exception class for all config validation issues."""

class FileError(ConfigError):
    """Exception class for IOReader issues."""

class ConfigStructureError(ConfigError):
    """Config exception class for config structure issues."""

class ConfigValuesError(ConfigError):
    """Config exception class for config values issues."""

class InputError(Exception):
    """Exception class for all input validation issues."""

class InputStructureError(InputError):
    """Input exception class for input structure issues."""

class InputValuesError(InputError):
    """Input exception class for input values issues."""