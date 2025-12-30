from core.utils.type_aliases import (
    CommandClass, CommandType, ConfigType, InternalCommandStates
)

from core.command import CommandNode, AliasNode, StateNode
from core.factories import CommandNodeFactory
from core.commands_config import CommandsConfig

from typing import Dict, List, Any, cast, get_args

class Parser:
    """This class parses raw data to intermediate reference."""

    @staticmethod
    def parse_commands(commands: Dict[str, CommandClass]) -> List[CommandNode]:
        def parse_command(name: str, command_dict: CommandClass) -> CommandNode:
            command_type: CommandType = command_dict.get("type")
            aliases: List[AliasNode] = []
            default: Any = None
            children: List[CommandNode] = []

            if command_type in ("word", "flag", "option"):
                aliases = [AliasNode(name, alias) for alias in command_dict.get("aliases", [])]
            
            if command_type in ("flag", "option"):
                default: Any = command_dict.get("default", None)
            
            if command_type in ("word", "fallback"):
                children: List[CommandNode] = []
            
                for child_name, child_dict in command_dict.get("children", {}).items():
                    children.append(parse_command(child_name, cast(CommandClass, child_dict)))
            
            return CommandNodeFactory.create(name, command_type, aliases, default, children)

        return [parse_command(name, command_dict) for name, command_dict in commands.items()]
    
    @staticmethod
    def parse_states(states_dict: Dict[str, List[str]]) -> List[StateNode]:
        return [
            StateNode(state, state in get_args(InternalCommandStates), aliases)
            for state, aliases in states_dict.items()
        ]
    
    @staticmethod
    def parse_config(config_dict: ConfigType) -> CommandsConfig:
        return CommandsConfig(
            config_dict["version"],
            Parser.parse_states(config_dict["states"]),
            Parser.parse_commands(config_dict["commands"])
        )