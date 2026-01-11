# pyright: reportUnnecessaryIsInstance=false
# ^^^^^^^ (Raw dynamic data checking.)

from core.utils.type_aliases import (
    ConfigType, UnknownConfigType, ConfigVersion, UnknownCommandClass, CommandClass, CommandType, CommandConfig_Unknown,
    CommandStates, InternalCommandStates
)
from core.utils.enums import ConfigVersions, WarningsLevel
from core.utils.lib_warnings import ConfigStructureWarning, ConfigValuesWarning, ConfigStructureError, ConfigValuesError
from core.utils.constants import Constants, Strings
from core.utils.functions import warning

from core.settings import Settings

from typing import Dict, get_args, Optional, List, Any

from string import punctuation

class ConfigValidator:
    """Validator class for config structure and semantic."""

    empty_name_replace_index: int = -1

    @staticmethod
    def validate_version(settings: Settings, config_dict: UnknownConfigType) -> ConfigVersion:
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
    def validate_command_type(settings: Settings, command_dict: UnknownCommandClass) -> Optional[CommandType]:
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
                ' ' + Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigValuesWarning,
                ConfigValuesError
            )
        
        return command_type
    
    @staticmethod
    def validate_command_aliases(settings: Settings, command_dict: UnknownCommandClass) -> List[str]:
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
        if "default" in command_dict:
            return command_dict["default"]
        return None
    
    @staticmethod
    def validate_command(settings: Settings, command_dict: UnknownCommandClass) -> Optional[CommandClass]:
        command_type: Optional[CommandType] = ConfigValidator.validate_command_type(settings, command_dict)
        if command_type is None:
            return None
        
        arguments: CommandConfig_Unknown = {
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
    def validate_name(settings: Settings, name: str, is_state: bool=False, is_fallback: bool=False) -> str:
        if name == ''.join([" "] * len(name)):
            warning(
                settings,
                Strings.COMMAND_NAME_EMPTY,
                Strings.AUTO_CORRECT_WITH_REMOVING,
                ConfigValuesWarning,
                ConfigValuesError
            )
            ConfigValidator.empty_name_replace_index += 1
            return f"command+{ConfigValidator.empty_name_replace_index}"

        i: int = 0
        found_letter: bool = False
        found_dollar: bool = False
        removing_indexes: List[int] = []
        specials = set(punctuation)
        specials.add(' ')
        specials.remove('-')
        while i < len(name):
            if name[i] == '-' and not found_letter:
                warning(
                    settings,
                    Strings.COMMAND_NAME_STARTS_INVALID,
                    Strings.AUTO_CORRECT_WITH_REMOVING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )
                removing_indexes.append(i)
            elif name[i] in specials:
                if is_state and name[i] == "_":
                    start: int = i
                    while i < len(name) and name[i] == "_":
                        i += 1
                    if i - start == 2:
                        continue
                    warning(
                        settings,
                        Strings.STATE_INTERNAL_NAME_INVALID.substitute(length=(i - start)),
                        Strings.AUTO_CORRECT_TO_DEFAULTS,
                        ConfigValuesWarning,
                        ConfigValuesError
                    )
                    name = name[:start] + "__" + name[i:]
                    i = start + 2
                
                if is_fallback and name[i] == "$":
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
                found_letter = True
            else:
                warning(
                    settings,
                    Strings.UNKNOWN_CHARACTER.substitute(character=name[i]),
                    Strings.AUTO_CORRECT_WITH_SKIPPING,
                    ConfigValuesWarning,
                    ConfigValuesError
                )

            i += 1
        
        for index in reversed(removing_indexes):
            name = name[:index] + name[index + 1:]
        
        if is_fallback and not found_dollar:
            warning(
                settings,
                Strings.COMMAND_FALLBACK_DOLLAR_NOT_FOUND,
                '',
                ConfigValuesWarning,
                warning_levels=(WarningsLevel.Basic, WarningsLevel.Strict),
                exception_levels=(None,)
            )
        
        return name

    @staticmethod
    def validate_commands(settings: Settings, config_dict: UnknownConfigType) -> Dict[str, CommandClass]:
        commands: Dict[str, CommandClass] = {}
        used_aliases: List[str] = []

        if "commands" in config_dict:
            if isinstance(config_dict["commands"], dict):
                for key, command_dict in config_dict["commands"].items():
                    key = ConfigValidator.validate_name(
                        settings,
                        key,
                        is_fallback=(command_dict.get("type") == "fallback")
                    )

                    command: Optional[CommandClass] = ConfigValidator.validate_command(settings, command_dict)
                    if command:
                        new_aliases: List[str] = []
                        if "aliases" in command_dict:
                            for alias in command_dict["aliases"]:
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
            else:
                warning(
                    settings,
                    Strings.INVALID_CONFIG_COMMANDS,
                    Strings.AUTO_CORRECT_TO_DEFAULTS,
                    ConfigStructureWarning,
                    ConfigStructureError
                )
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_COMMANDS,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            
        return commands
    
    @staticmethod
    def get_command_keys(commands: Dict[str, CommandClass]) -> List[str]:
        # Unused method, but may help in future. #

        def process_command(command: CommandClass) -> List[str]:
            command_keys: List[str] = []

            if "children" in command:
                for key, next_command in command["children"].items():
                    command_keys.append(key)
                    command_keys.extend(process_command(next_command))
            
            return command_keys

        keys: List[str] = []

        for key, command_dict in commands.items():
            keys.append(key)

            if "children" in command_dict:
                keys.extend(process_command(command_dict))

        return keys
    
    @staticmethod
    def validate_states(
        settings: Settings,
        config_dict: UnknownConfigType,
        commands: Dict[str, CommandClass]
    ) -> CommandStates:
        states: CommandStates = {}

        command_names: List[str] = [key for key in commands.keys()]

        if "states" in config_dict:
            if isinstance(config_dict["states"], dict):
                for state, names in config_dict["states"].items():
                    state = ConfigValidator.validate_name(settings, state, is_state=True)

                    if state.startswith("__") and state.endswith("__") and state not in get_args(InternalCommandStates):
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
                        name = ConfigValidator.validate_name(settings, name)

                        if name not in command_names:
                            warning(
                                settings,
                                Strings.COMMAND_UNKNOWN_NAME,
                                Strings.AUTO_CORRECT_WITH_SKIPPING,
                                ConfigValuesWarning,
                                ConfigValuesError
                            )
                        else:
                            states[state].append(name)
            else:
                warning(
                    settings,
                    Strings.INVALID_CONFIG_STATES,
                    Strings.AUTO_CORRECT_TO_DEFAULTS,
                    ConfigStructureWarning,
                    ConfigStructureError
                )
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_STATES,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                ConfigStructureError
            )
            states["__base__"] = command_names

        return states
    
    @staticmethod
    def validate_config(settings: Settings, config_dict: UnknownConfigType) -> ConfigType:
        version: ConfigVersion = ConfigValidator.validate_version(settings, config_dict)
        commands: Dict[str, CommandClass] = ConfigValidator.validate_commands(settings, config_dict)
        states: CommandStates = ConfigValidator.validate_states(settings, config_dict, commands)

        return {"version": version, "states": states, "commands": commands}