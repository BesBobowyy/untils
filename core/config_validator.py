# pyright: reportUnnecessaryIsInstance=false

from core.utils.type_aliases import (
    ConfigType, UnknownConfigType, ConfigVersion, UnknownCommandClass, CommandClass, CommandType, CommandConfig_Unknown,
    CommandStates, InternalCommandStates
)
from core.utils.enums import ConfigVersions
from core.utils.lib_warnings import ConfigStructureWarning, ConfigValuesWarning
from core.utils.constants import Constants, Strings
from core.utils.functions import warning

from core.settings import Settings

from typing import Dict, get_args, Optional, List, Any

class ConfigValidator:
    """Validator class for config structure and semantic."""

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
                    ValueError
                )
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_VERSION.substitute(version=Strings.UNKNOWN_VERSION),
                Strings.AUTO_CORRECT_TO_LATEST,
                ConfigStructureWarning,
                KeyError
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
                    ValueError
                )
        else:
            warning(
                settings,
                Strings.COMMAND_UNKNOWN_TYPE,
                ' ' + Strings.AUTO_CORRECT_WITH_SKIPPING,
                ConfigValuesWarning,
                KeyError
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
                    TypeError
                )
            else:
                for alias in command_dict["aliases"]:
                    if not isinstance(alias, str):
                        warning(
                            settings,
                            Strings.COMMAND_ALIAS_INVALID.substitute(alias=alias),
                            Strings.AUTO_CORRECT_WITH_CASTING,
                            ConfigValuesWarning,
                            TypeError
                        )
                        alias = str(alias)

                    if alias in aliases:
                        warning(
                            settings,
                            Strings.COMMAND_ALIAS_COPIED.substitute(alias=alias),
                            Strings.AUTO_CORRECT_WITH_SKIPPING,
                            ConfigValuesWarning,
                            ValueError
                        )
                    
                    aliases.append(alias)
        
        return aliases

    @staticmethod
    def validate_command_default(settings: Settings, command_dict: UnknownCommandClass) -> Any:
        if "default" in command_dict:
            return command_dict["default"]
        
        warning(
            settings,
            Strings.COMMAND_INVALID_DEFAULT,
            Strings.AUTO_CORRECT_TO_DEFAULTS,
            ConfigStructureWarning,
            KeyError
        )
    
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

        if command_type in ("flag", "option"):
            arguments["default"] = ConfigValidator.validate_command_default(settings, command_dict)

        if command_type in ("word", "fallback"):
            arguments["children"] = {}

            if "children" in command_dict:
                for k, cd in command_dict["children"].items():
                    child: Optional[CommandClass] = ConfigValidator.validate_command(settings, cd)
                    
                    if child is not None:
                        arguments["children"][k] = child
                
                if arguments["children"] == {}:
                    warning(
                        settings,
                        Strings.COMMAND_INVALID_CHILDREN,
                        Strings.AUTO_CORRECT_WITH_REMOVING,
                        ConfigValuesWarning,
                        ValueError
                    )
        
        return arguments    # pyright: ignore[reportReturnType] (The arguments are always correct.)
    
    @staticmethod
    def validate_commands(settings: Settings, config_dict: UnknownConfigType) -> Dict[str, CommandClass]:
        commands: Dict[str, CommandClass] = {}

        if "commands" in config_dict:
            for key, command_dict in config_dict["commands"].items():
                command: Optional[CommandClass] = ConfigValidator.validate_command(settings, command_dict)
                if command:
                    commands[key] = command
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_COMMANDS,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                KeyError
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
            for state, names in config_dict["states"].items():
                if state.startswith("__") and state.endswith("__") and state not in get_args(InternalCommandStates):
                    warning(
                        settings,
                        Strings.STATE_INVALID_NAME,
                        Strings.AUTO_CORRECT_WITH_RENAMING,
                        ConfigValuesWarning,
                        NameError
                    )
                    state = '+' + state

                states[state] = []
                
                for name in names:
                    if name not in command_names:
                        warning(
                            settings,
                            Strings.COMMAND_UNKNOWN_NAME,
                            Strings.AUTO_CORRECT_WITH_SKIPPING,
                            ConfigValuesWarning,
                            NameError
                        )
                    else:
                        states[state].append(name)
                        
        else:
            warning(
                settings,
                Strings.INVALID_CONFIG_STATES,
                Strings.AUTO_CORRECT_TO_DEFAULTS,
                ConfigStructureWarning,
                KeyError
            )
            states["__base__"] = command_names

        return states
    
    @staticmethod
    def validate_config(settings: Settings, config_dict: UnknownConfigType) -> ConfigType:
        version: ConfigVersion = ConfigValidator.validate_version(settings, config_dict)
        commands: Dict[str, CommandClass] = ConfigValidator.validate_commands(settings, config_dict)
        states: CommandStates = ConfigValidator.validate_states(settings, config_dict, commands)

        return {"version": version, "states": states, "commands": commands}



if __name__ == "__main__":
    from core.utils.type_aliases import UnknownConfigType

    from core.ioreader import IOReader

    import os

    FILE_PATH: str = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "examples",
        "resources",
        "commands_1.json"
    )
    SETTINGS: Settings = Settings()

    content: UnknownConfigType = IOReader.read_file(SETTINGS, FILE_PATH)

    config_raw: ConfigType = ConfigValidator.validate_config(SETTINGS, content)
    print(config_raw)