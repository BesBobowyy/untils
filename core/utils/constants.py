from core.utils.enums import LibraryVersionStatus, ConfigVersions

from typing import Tuple, Literal

from string import Template

class Constants:
    """The library constants."""

    SUPPORTED_CONFIG_FORMATS: Tuple[Literal[".json", ".json5"], ...] = (".json", ".json5")
    """All config formats, which supported in current version of the library."""
    
    STANDART_CONFIG_FORMATS: Tuple[Literal['.json']] = (".json",)
    """All standart config format, which must be used in final product."""

    LATEST_CONFIG_VERSION = ConfigVersions.V1
    """Current config version."""

    VERSION: Tuple[Literal[1], Literal[0], Literal[0], Literal[LibraryVersionStatus.d]] = (1, 0, 0, LibraryVersionStatus.d)
    """Current library version."""

class Strings:
    """The library strings."""

    UNKNOWN_VERSION = "<unknown>"
    """Unknown version identifier."""

    ANY_VERSION = "<any>"
    """Any version identifier."""

    REMOVED_METHOD = "Removed method's body, shall be replaced."
    """This method was removed and hasn't implementations."""

    DEPRECATED_METHOD = "Deprecated method, may be removed in future."
    """This method must be replaced to other, but now works."""

    ALTERNATIVE_METHOD = "Alternative method, it is not in standart, but is stable."
    """This method is stable, but can be replaced to standart analog."""

    CONFIG_FILE_NOT_EXISTS = "The config file is not exists."
    """Config file didn't found by it's path."""

    CONFIG_EXTENSION_NOT_SUPPORTS = "The config file extension is not supported. Try to use another format or dictionary."
    """Config file not supported by IOReader."""

    AUTO_CORRECT_TO_LATEST = "Auto-correcting to the latest."
    """Auto-correcting to the latest version of something."""

    AUTO_CORRECT_TO_DEFAULTS = "Auto-correcting to default."
    """Auto-correcting to the dafault value of something."""

    AUTO_CORRECT_WITH_REMOVING = "Auto-correcting with removing."
    """Auto-correcting with removing of something."""

    AUTO_CORRECT_WITH_SKIPPING = "Skipping."
    """Auto-correcting with ignore of something."""

    AUTO_CORRECT_WITH_ACCEPTING = "Accepting, but try to use other variant later."
    """Auto-correcting with accepting of something."""

    AUTO_CORRECT_WITH_CASTING = "Auto-correcting to correct type."
    """Auto-correcting to correct type."""

    AUTO_CORRECT_WITH_RENAMING = "Auto-correcting to first available name."
    """Auto-correcting to first available name."""

    INVALID_CONFIG_VERSION: Template = Template("Config version $version is not valid. Change to the latest with migration.")
    """String: \"The config version $version is not valid. Change to the latest with migration.\"

    The config version is not supported, must be changed.
    
    Placeholders:
        $version - The version number.
    """

    INVALID_CONFIG_STATES = "The config states signature are not valid."
    """The config states signature are not valid."""

    INVALID_CONFIG_COMMANDS = "The config commands did not written."
    """The config commands did not written."""

    STATE_INVALID_NAME = "You cannot use an internal state name singature."
    """You cannot use an internal state name singature."""

    STATE_INTERNAL_NAME_INVALID: Template = Template("Expected length 2 of the special internal state name character, got $length.")
    """String: \"Expected length 2 of the special internal state name character, got $length.\"
    
    Invalid internal state name signature.
    
    Placeholders:
        $length - Length of special characters sequence.
    """

    COMMAND_UNKNOWN_NAME = "Command name is not valid."
    """Command name is not valid."""

    COMMAND_UNKNOWN_TYPE = "Command type did not written."
    """Command type did not written."""

    COMMAND_INVALID_TYPE = "The command type is not valid."
    """Command type is not valid."""

    COMMAND_INVALID_DEFAULT = "Command default value did not written."
    """Command default value did not written."""

    COMMAND_UNKNOWN_ALIASES = "Command aliases did not written."
    """Command aliases did not written."""

    COMMAND_INVALID_ALIASES = "The command aliases must be list with strings."
    """The command aliases must be list with strings."""

    COMMAND_ALIAS_COPIED: Template = Template("The command alias \'$alias\' was duplicated.")
    """String: \"The command alias \'$alias\' was duplicated.\"
    
    Placeholders:
        $alias - The alias name.
    """

    COMMAND_ALIAS_REDUNDANCY: Template = Template("The command alias \"$alias\" is copying an original name.")
    """String: \"The command alias \"$alias\" is copying an original name.\"
    
    Placeholders:
        $alias - The alias name.
    """

    COMMAND_ALIAS_INVALID: Template = Template("The command alias \"$alias\" is not string.")
    """String: \"The command alias \"$alias\" is not string.\"

    The alias type is not valid.
    
    Placeholders:
        $alias - The alias name.
    """

    COMMAND_INVALID_CHILDREN = "The command children is written, but empty."
    """The command children is written, but empty."""

    COMMAND_NAME_EMPTY = "The command name is empty."
    """The command name is empty."""

    COMMAND_NAME_STARTS_INVALID = "The command name starts from '-'."
    """The command name starts from '-'."""

    COMMAND_NAME_SPECIAL: Template = Template("The command name uses the blocked special character \'$character\'.")
    """String: \"The command name uses the blocked special character \'$character\'.\"
    
    The command name contains special characters.
    
    Placeholders:
        $character - The special character.
    """

    COMMAND_NOT_IN_CURRENT_STATE: Template = Template("The command is not defined in the current state '$state' or in the '__base__' state.")
    """String: \"The command is not defined in the current state '$state' or in the '__base__' state.\"
    
    The command not in current context.

    Placeholders:
        $state - The state name.
    """

    COMMAND_FALLBACK_DOLLAR_NOT_FOUND = "The `Fallback` command may has a single \'$\' character on name start by the standart, but it is not found."
    """The `Fallback` command must be has the \'$\' symbol on name start, but it is only for readability."""

    COMMAND_FALLBACK_DOLLAR_OVERLOAD = "The `Fallback` command has several \'$\' character."
    """The `Fallback` command cannot has several \'$\' symbols in name."""

    COMMAND_FALLBACK_DOLLAR_MISPOSITION = "The `Fallback` command has \'$\' character not on start."
    """The `Fallback` command must be has the \'$\' symbol only on name start."""

    UNKNOWN_CHARACTER: Template = Template("Unknown character '$character'.")
    """String: \"Unknown character '$character'.\"
    
    Placeholders:
        $character - Unknown character.
    """

    END_OF_INPUT = "End of input."
    """Expected next token, got end of input."""

    TOKEN_MINUS_OVERFLOW: Template = Template("The `Minus` token has count $count overflow.")
    """String: \"`The `Minus` token has count $count overflow.\"

    The `Minus` token defines a next token signature, but it can be only 1 or 2 in a row.
    
    Placeholders:
        $count - Count of tokens.
    """

    EXPECTED_TOKEN: Template = Template("Expected $expected token, got $token.")
    """String: \"Expected $expected token, got $token.\"
    
    Placeholders:
        $expected - Expected token.
        $token - Got token.
    """

    EXPECTED_SYNTAX_FLAG = "Expected `Flag` token syntax."
    """Expected `Flag` token syntax."""

    EXPECTED_SYNTAX_OPTION = "Expected `Option` token syntax."
    """Expected `Option` token syntax."""

    UNKNOWN_TOKEN = "Got unknown token."
    """Got unknown token."""

    OPTION_NAME_INVALID = "The option's name is not valid."
    """The option's name is not valid."""

    OPTION_VALUE_INVALID = "The option's value is not valid."
    """The option's value is not valid."""

    INPUT_PATH_INVALID: Template = Template("A command with name \'$name\' is not found.")
    """String: \"A command with name \'$name\' is not found.\"

    Expected a command with unknown name.

    Placeholders:
        $name - A command name.
    """