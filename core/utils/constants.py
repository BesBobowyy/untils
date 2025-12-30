from core.utils.enums import ConfigVersions

from typing import Tuple, Literal

from string import Template

class Constants:
    """Class-container for every constants."""

    SUPPORTED_CONFIG_FORMATS: Tuple[Literal[".json", ".json5"], ...] = (".json", ".json5")
    
    STANDART_CONFIG_FORMATS: Tuple[Literal['.json']] = (".json",)

    LATEST_CONFIG_VERSION = ConfigVersions.V1

class Strings:
    """Class-container for every message."""

    UNKNOWN_VERSION = "<unknown>"
    """Unknown version identifier."""

    ANY_VERSION = "<any>"
    """Any version identifier."""

    REMOVED_METHOD = "Removed method, shall be replaced."
    """This method or function was removed and hasn't body."""

    DEPRECATED_METHOD = "Deprecated method."
    """This method or function must be replaced to another."""

    ALTERNATIVE_METHOD = "Alternative non-standart method."
    """This method or function is stable, but can be replaced to standart analog."""

    CONFIG_FILE_NOT_EXISTS = "The config file is not exists."
    """Config file didn't found by path."""

    CONFIG_EXTENSION_NOT_SUPPORTS = "The config file extension is not supports. Try to use supported format or dict."
    """Config file not supports by IOReader."""

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

    INVALID_CONFIG_VERSION: Template = Template("Config version $version is not valid.")
    """String: \"Config version $version is not valid.\"
    
    Placeholders:
        $version - Version number.
    """

    INVALID_CONFIG_STATES = "Config states are invalid."
    """Config states signature is not valid."""

    INVALID_CONFIG_COMMANDS = "Config commands didn't written."
    """Config commands didn't written."""

    STATE_INVALID_NAME = "You cannot use internal state name format."
    """Used unknown internal state name."""

    COMMAND_UNKNOWN_NAME = "Command name is not valid."
    """Command name not available."""

    COMMAND_UNKNOWN_TYPE = "Command type didn't written."
    """Command type didn't written."""

    COMMAND_INVALID_TYPE = "Command type is not valid."
    """Command type invalid."""

    COMMAND_INVALID_DEFAULT = "Command default value didn't written."
    """Command default value didn't written, but it must be written."""

    COMMAND_UNKNOWN_ALIASES = "Command aliases didn't written."
    """Command aliases didn't written."""

    COMMAND_INVALID_ALIASES = "Command aliases must be a list with strings."
    """Commands aliases invalid."""

    COMMAND_ALIAS_COPIED: Template = Template("Command alias \"$alias\" was duplicated.")
    """String: \"Command alias \"$alias\" was duplicated.\"
    
    Placeholders:
        $alias - Alias name.
    """

    COMMAND_ALIAS_REDUNDANCY: Template = Template("Command alias \"$alias\" is copying original name.")
    """String: \"Command alias \"$alias\" is copying original name.\"
    
    Placeholders:
        $alias - Alias name.
    """

    COMMAND_ALIAS_INVALID: Template = Template("Command alias $alias not string.")
    """String: \"Command alias $alias not string.\"

    Alias type invalid.
    
    Placeholders:
        $alias - Alias name.
    """

    COMMAND_INVALID_CHILDREN = "Command children is empty, but written."
    """Command children is empty, but the children body was written."""

    COMMAND_NAME_EMPTY = "Command name is empty."
    """Command name is empty."""

    COMMAND_NAME_STARTS_INVALID = "Command name starts from '-', which denied."
    """Command name starts with incorrect characters."""

    COMMAND_NAME_SPECIAL: Template = Template("Command name uses special character '$character', which denied.")
    """String: \"Command name uses special character '$character', which denied.\"
    
    Command name contains special characters.
    
    Placeholders:
        $character - Special character.
    """