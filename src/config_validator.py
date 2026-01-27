"""config_validator.py - Deep config validation."""

# pyright: reportUnnecessaryIsInstance=false
# ^^^^^^^ (Raw dynamic data checking.)

from typing import Dict, get_args, Optional, List, Any

from string import punctuation

from src.utils.type_aliases import (
    ConfigType, UnknownConfigType, ConfigVersion, UnknownCommandClass, CommandClass, CommandType,
    UnknownCommandConfig, CommandStates, InternalCommandStates
)
from src.utils.enums import ConfigVersions, WarningsLevel
from src.utils.lib_warnings import (
    ConfigStructureWarning, ConfigValuesWarning, ConfigStructureError, ConfigValuesError
)
from src.utils.constants import Constants, Strings
from src.utils.functions import warning

from src.settings import Settings

class ConfigValidator:
    """Validator class for config structure and semantic."""

    _empty_name_replace_index: int = -1
    """Private variable, which uses for invalid names renaming. It prevents name duplication."""

    @staticmethod
    def validate_version(settings: Settings, config_dict: UnknownConfigType) -> ConfigVersion:
        """Validates the config version.
        
        Args:
            settings: The settings.
            config_dict: The config dictionary, which was not validated yet.
        
        Returns:
            `ConfigVersion` if config version is valid, else returns the latest version in `Constants.LATEST_CONFIG_VERSION`.

        Raises:
            ConfigStructureWarning: `version` field is not found in config.
            ConfigValuesWarning: Config version is not supported or invalid.

            ConfigStructureError: `version` field is not found in config.
            ConfigValuesError: Config version is not supported or invalid.
        """

        version: int = -1

        if "version" in config_dict:
            version = config_dict["version"]

            if version not in ConfigVersions:
                warning(
                    settings,
                    Strings.INVALID_CONFIG_VERSION.substitute(version=repr(version)),
                    Strings.AUTO_CORRECT_TO_LATEST,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_VERSION.substitute(version=Strings.UNKNOWN_VERSION),
                Strings.AUTO_CORRECT_TO_LATEST,
                ConfigStructureWarning,
                ConfigStructureError
            )
            version = Constants.LATEST_CONFIG_VERSION.value

        return version

    @staticmethod
    def validate_command_type(
        settings: Settings,
        command_dict: UnknownCommandClass
    ) -> Optional[CommandType]:
        """Validates a command type.
        
        Args:
            settings: The settings.
            command_dict: The command dictionary, which was not validated yet.
        
        Returns:
            `CommandType` if the command type was validated successfully, else `None`.
        
        Raises:
            ConfigValuesWarning: The command type field is not written.

            ConfigValuesErorr: The command type is not valid or unknown.
        """

        command_type: Optional[CommandType] = None

        if "type" in command_dict:
            if command_dict["type"] in get_args(CommandType):
                command_type = command_dict["type"]
            else:
                warning(
                    settings,
                    Strings.COMMAND_INVALID_TYPE,
                    Strings.AUTO_CORRECT_WITH_SKIPPING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
        else:
            warning(
                settings,
                Strings.COMMAND_UNKNOWN_TYPE,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigStructureWarning,
                ConfigStructureError
            )

        return command_type

    @staticmethod
    def validate_command_aliases(
        settings: Settings,
        command_dict: UnknownCommandClass
    ) -> List[str]:
        """Validates command aliases from a command dictionary.
        
        Args:
            settings: The settings.
            command_dict: The command dictionary, which was not validated yet.

        Returns:
            Returns validated aliases.

        Raises:
            ConfigStructureWarning: The command aliases are not written or is not list.
            ConfigValuesWarning: An alias in the command aliases is not string or duplicates previous.

            ConfigStructureError: The command aliases are not written or is not list.
            ConfigValuesError: An alias in the command aliases is not string or duplicates previous.
        """

        aliases: List[str] = []

        if "aliases" in command_dict:
            if not isinstance(command_dict["aliases"], list):
                warning(
                    settings,
                    Strings.COMMAND_INVALID_ALIASES,
                    Strings.AUTO_CORRECT_TO_DEFAULTS,
                    ConfigStructureWarning,
                    ConfigStructureError
                )
            else:
                for alias in command_dict["aliases"]:
                    if not isinstance(alias, str):
                        warning(
                            settings,
                            Strings.COMMAND_ALIAS_INVALID.substitute(alias=alias),
                            Strings.AUTO_CORRECT_WITH_CASTING,
                            ConfigValuesWarning,
                            ConfigValuesError
                        )
                        alias = str(alias)

                    if alias in aliases:
                        warning(
                            settings,
                            Strings.COMMAND_ALIAS_COPIED.substitute(alias=alias),
                            Strings.AUTO_CORRECT_WITH_SKIPPING,
                            ConfigValuesWarning,
                            ConfigValuesError
                        )

                    aliases.append(alias)

        return aliases

    @staticmethod
    def validate_command_default(command_dict: UnknownCommandClass) -> Any:
        """Validates a command default value.
        
        Args:
            command_dict: The command dictionary, which was not validated yet.
        
        Returns:
            `Any` if the default value is exists, else `None`.
        """

        if "default" in command_dict:
            return command_dict["default"]
        return None

    @staticmethod
    def validate_command(
        settings: Settings,
        command_dict: UnknownCommandClass
    ) -> Optional[CommandClass]:
        """Validates a command dictionary.
        
        Args:
            settings: The settings.
            command_dict: The command dictionary, which was not validated yet.
        
        Returns:
            `CommandClass` if command was validated successfully, else `None`. Also `None` returns if a type field is not written or required fields for this type are not written.
        
        Raises:
            ConfigStructureWarning: Structure of the command is not valid.
            ConfigValuesWarning: The command values is not valid.

            ConfigStructureError: Structure of the command is not valid.
            ConfigValuesError: The command values is not valid.
        """

        command_type: Optional[CommandType] = ConfigValidator.validate_command_type(
            settings,
            command_dict
        )
        if command_type is None:
            return None

        arguments: UnknownCommandConfig = {
            "type": command_type
        }

        if command_type in ("word", "flag", "option"):
            arguments["aliases"] = ConfigValidator.validate_command_aliases(settings, command_dict)

        if command_type not in ("word", "flag", "option") and "aliases" in command_dict:
            warning(
                settings,
                Strings.COMMAND_INVALID_TYPE,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return None

        if command_type in ("fallback", "flag", "option"):
            arguments["default"] = ConfigValidator.validate_command_default(command_dict)
        if command_type not in ("fallback", "flag", "option") and "default" in command_dict:
            warning(
                settings,
                Strings.COMMAND_INVALID_TYPE,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return None

        if command_type in ("word", "fallback"):
            arguments["children"] = {}

            if "children" in command_dict:
                for k, cd in command_dict["children"].items():
                    k = ConfigValidator.validate_name(
                        settings,
                        k,
                        is_fallback=(cd.get("type") == "fallback")
                    )
                    child: Optional[CommandClass] = ConfigValidator.validate_command(settings, cd)

                    if child is not None:
                        arguments["children"][k] = child

                if arguments["children"] == {}:
                    warning(
                        settings,
                        Strings.COMMAND_INVALID_CHILDREN,
                        Strings.AUTO_CORRECT_WITH_REMOVING,
                        ConfigValuesWarning,
                        ConfigValuesError
                    )
        if command_type not in ("word", "fallback") and "children" in command_dict:
            warning(
                settings,
                Strings.COMMAND_INVALID_TYPE,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return None

        return arguments    # pyright: ignore[reportReturnType] (The arguments are always correct.)

    @staticmethod
    def validate_name(
        settings: Settings,
        name: str,
        is_state: bool=False,
        is_fallback: bool=False
    ) -> str:
        """Validates an identifier name.
        
        Args:
            settings: The settings.
            name: The string name.
            is_state: Is this validation for state.
            is_fallback: Is this validation for the `Fallback` command type.

        Returns:
            Validated and corrected string name.

        Raises:
            ConfigValuesWarning: The name is empty, has '-' character in name start, has special characters, has invalid `InternalState` structure (if `is_state == True`), has invalid `Fallback` structure (if `is_fallback == True`) or character is not valid.

            ConfigValuesError: The name is empty, has '-' character in name start, has special characters, has invalid `InternalState` structure (if `is_state == True`), has invalid `Fallback` structure (if `is_fallback == True`) or character is not valid.
        """

        if not isinstance(name, str):
            warning(
                settings,
                Strings.COMMAND_INVALID_ALIASES,
                Strings.AUTO_CORRECT_WITH_CASTING,
                ConfigValuesWarning,
                ConfigValuesError
            )
            name = str(name)

        if name == ''.join([" "] * len(name)):
            warning(
                settings,
                Strings.COMMAND_NAME_EMPTY,
                Strings.AUTO_CORRECT_WITH_REMOVING,
                ConfigValuesWarning,
                ConfigValuesError
            )
            ConfigValidator._empty_name_replace_index += 1
            return f"command+{ConfigValidator._empty_name_replace_index}"

        i: int = 0
        found_letter: bool = False
        found_dollar: bool = False
        removing_indexes: List[int] = []
        specials = set(punctuation)
        specials.add(' ')
        specials.remove('-')
        while i < len(name):
            if name[i] == '-' and not found_letter:
                # '-' as invalid separator.
                warning(
                    settings,
                    Strings.COMMAND_NAME_STARTS_INVALID,
                    Strings.AUTO_CORRECT_WITH_REMOVING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
                removing_indexes.append(i)
            elif name[i] in specials:
                # Character is special.
                if is_state:
                    if name[i] == "_":
                        # Internal state name validation.
                        start: int = i
                        while i < len(name) and name[i] == "_":
                            i += 1
                        if i - start == 2:
                            continue
                        warning(
                            settings,
                            Strings.STATE_INTERNAL_NAME_INVALID.substitute(length=i - start),
                            Strings.AUTO_CORRECT_TO_DEFAULTS,
                            ConfigValuesWarning,
                            ConfigValuesError
                        )
                        name = name[:start] + "__" + name[i:]
                        i = start + 2
                    elif name[i] in ("-", ":", "/"):
                        # Allowed special characters in state name.
                        i += 1
                        continue

                if is_fallback and name[i] == "$":
                    # `Fallback` type standart.
                    if i == 0:
                        i += 1
                        found_dollar = True
                        continue

                    if i > 0 and not found_dollar:
                        warning(
                            settings,
                            Strings.COMMAND_FALLBACK_DOLLAR_MISPOSITION,
                            Strings.AUTO_CORRECT_WITH_REMOVING,
                            ConfigValuesWarning,
                            ConfigValuesError
                        )
                        found_dollar = True
                        name = name[:i] + name[i + 1:]
                        i += 1
                        continue

                    if found_dollar:
                        warning(
                            settings,
                            Strings.COMMAND_FALLBACK_DOLLAR_OVERLOAD,
                            Strings.AUTO_CORRECT_WITH_REMOVING,
                            ConfigValuesWarning,
                            ConfigValuesError
                        )
                        name = name[:i] + name[i + 1:]
                        i += 1
                        continue

                warning(
                    settings,
                    Strings.COMMAND_NAME_SPECIAL.substitute(character=name[i]),
                    Strings.AUTO_CORRECT_WITH_REMOVING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
                removing_indexes.append(i)
            elif name[i].isalnum():
                # Character is valid.
                found_letter = True
            else:
                # Character is unknown.
                warning(
                    settings,
                    Strings.UNKNOWN_CHARACTER.substitute(character=name[i]),
                    Strings.AUTO_CORRECT_WITH_SKIPPING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )

            i += 1

        # Deleting the removing character.
        for index in reversed(removing_indexes):
            name = name[:index] + name[index + 1:]

        if is_fallback and not found_dollar:
            # The `Fallback` standart warning.
            warning(
                settings,
                Strings.COMMAND_FALLBACK_DOLLAR_NOT_FOUND,
                '',
                ConfigValuesWarning,
                warning_levels=(WarningsLevel.BASIC, WarningsLevel.STRICT),
                exception_levels=(None,)
            )

        return name

    @staticmethod
    def validate_commands(
        settings: Settings,
        config_dict: UnknownConfigType
    ) -> Dict[str, CommandClass]:
        """Validates commands in the config field `commands`.
        
        Args:
            settings: The settings.
            config_dict: The config dictionary, which was not validated yet.

        Returns:
            Validated commands in stable and known format.

        Raises:
            ConfigStructureWarning: The `commands` field is not written or not dict.
            ConfigValuesWarning: Command aliases are duplicating or equals original command name.

            ConfigStructureError: The `commands` field is not written or not dict.
            ConfigValuesError: Command aliases are duplicating or equals original command name.
        """

        commands: Dict[str, CommandClass] = {}
        used_aliases: List[str] = []

        if "commands" not in config_dict:
            warning(
                settings,
                Strings.INVALID_CONFIG_COMMANDS,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return {}

        if not isinstance(config_dict["commands"], dict):
            warning(
                settings,
                Strings.INVALID_CONFIG_COMMANDS,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return {}

        for key, command_dict in config_dict["commands"].items():
            # Processing a branch of command.
            key = ConfigValidator.validate_name(
                settings,
                key,
                is_fallback=(command_dict.get("type") == "fallback")
            )

            command: Optional[CommandClass] = ConfigValidator.validate_command(
                settings,
                command_dict
            )
            if command:
                new_aliases: List[str] = []

                if "aliases" in command_dict:
                    for alias in command_dict["aliases"]:
                        # Processing an alias in the command aliases.
                        alias = ConfigValidator.validate_name(settings, alias)

                        if alias in used_aliases:
                            warning(
                                settings,
                                Strings.COMMAND_ALIAS_COPIED.substitute(alias=alias),
                                Strings.AUTO_CORRECT_WITH_REMOVING,
                                ConfigValuesWarning,
                                ConfigValuesError
                            )
                        elif alias == key:
                            warning(
                                settings,
                                Strings.COMMAND_ALIAS_REDUNDANCY.substitute(alias=alias),
                                Strings.AUTO_CORRECT_WITH_REMOVING,
                                ConfigValuesWarning,
                                ConfigValuesError
                            )
                        else:
                            used_aliases.append(alias)
                            new_aliases.append(alias)

                    command_dict["aliases"] = new_aliases

                key = ConfigValidator.validate_name(settings, key)
                commands[key] = command

        return commands

    @staticmethod
    def validate_states(
        settings: Settings,
        config_dict: UnknownConfigType,
        commands: Dict[str, CommandClass]
    ) -> CommandStates:
        """Validates config states.
        
        Args:
            settings: The settings.
            config_dict: The config dictionary, which was not validated yet.
            commands: The proccessed commands dict.

        Returns:
            Validated command states.

        Raises:
            ConfigStructureWarning: The config has not the field `states` or the states type is not dict.
            ConfigValuesWarning: An internal state by format is not written in `InternalCommandStates` or a command name is unknown.

            ConfigStructureError: The config has not the field `states` or the states type is not dict.
            ConfigValuesError: An internal state by format is not written in `InternalCommandStates` or a command name is unknown.
        """

        states: CommandStates = {}

        command_names: List[str] = [key for key in list(commands.keys())]

        if not "states" in config_dict:
            warning(
                settings,
                Strings.INVALID_CONFIG_STATES,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return {
                "__base__": command_names
            }

        if not isinstance(config_dict["states"], dict):
            warning(
                settings,
                Strings.INVALID_CONFIG_STATES,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            return {
                "__base__": command_names
            }

        for state, names in config_dict["states"].items():
            # Proccessing a state with their command names.
            state = ConfigValidator.validate_name(settings, state, is_state=True)

            if (
                state.startswith("__")
                and state.endswith("__")
                and state not in get_args(InternalCommandStates)
            ):
                # An internal state is not written in `InternalCommandStates`.
                warning(
                    settings,
                    Strings.STATE_INVALID_NAME,
                    Strings.AUTO_CORRECT_WITH_RENAMING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
                state = state[:2] + state[2:-2]

            states[state] = []

            for name in names:
                # Processing a command in the state.
                name = ConfigValidator.validate_name(settings, name)

                if name not in command_names:
                    # Unknown command name.
                    warning(
                        settings,
                        Strings.COMMAND_UNKNOWN_NAME,
                        Strings.AUTO_CORRECT_WITH_SKIPPING,
                        ConfigValuesWarning,
                        ConfigValuesError
                    )
                else:
                    states[state].append(name)

        return states

    @staticmethod
    def validate_config(settings: Settings, config_dict: UnknownConfigType) -> ConfigType:
        """Validates a raw config.
        
        Args:
            settings: The settings.
            config_dict: The config dictionary, which was not validated yet.

        Returns:
            Validated config.
        """

        version: ConfigVersion = ConfigValidator.validate_version(settings, config_dict)
        commands: Dict[str, CommandClass] = ConfigValidator.validate_commands(settings, config_dict)
        states: CommandStates = ConfigValidator.validate_states(settings, config_dict, commands)

        return {
            "version": version,
            "states": states,
            "commands": commands
        }
