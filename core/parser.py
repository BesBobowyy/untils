from core.utils.type_aliases import CommandClass, CommandType, ConfigType, InternalCommandStates, InputDict
from core.utils.protocols import FinalInputProtocol
from core.utils.enums import FinalTokenType

from core.command import CommandNode, AliasNode, StateNode
from core.factories import CommandNodeFactory
from core.commands_config import CommandsConfig
from core.input_token import FinalInputTokenWord, FinalInputTokenFlag, FinalInputTokenOption
from core.settings import Settings

from typing import Dict, List, Any, cast, get_args, Optional

class Parser:
    """This class parses raw data to intermediate reference."""

    @staticmethod
    def parse_commands(commands: Dict[str, CommandClass]) -> List[CommandNode]:
        """Parses a command dictionary to the AST tree of command nodes.
        
        Args:
            commands: The commands dictionary.

        Returns:
            Parsed AST tree of the command nodes.
        """

        def parse_command(name: str, command_dict: CommandClass) -> CommandNode:
            """Parses a single command.
            
            Args:
                name: The command name.
                command_dict: The command dictionary.

            Returns:
                The command node.
            """

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
        """Parses states in config.
        
        Args:
            states_dict: The states dictionary.

        Returns:
            The list of the state nodes.
        """

        return [
            StateNode(state, state in get_args(InternalCommandStates), aliases)
            for state, aliases in states_dict.items()
        ]
    
    @staticmethod
    def parse_config(config_dict: ConfigType) -> CommandsConfig:
        """Parses a validated config.
        
        Args:
            config_dict: The config dictionary.

        Returns:
            The parsed config.
        """

        return CommandsConfig(
            config_dict["version"],
            Parser.parse_states(config_dict["states"]),
            Parser.parse_commands(config_dict["commands"])
        )
    
    @staticmethod
    def parse_input(settings: Settings, tokens: List[FinalInputProtocol]) -> InputDict:
        """Parses a user input to input dictionary.
        
        Args:
            tokens: Final tokenized tokens.
            debug: Determines debug messages display.

        Returns:
            The parsed input dictionary.
        """

        settings.logger.debug(f"Parser.parse_input(tokens={tokens}).")

        path: List[str] = []
        flags: Dict[str, Optional[bool]] = {}
        options: Dict[str, Any] = {}

        i: int = 0
        while i < len(tokens):
            settings.logger.debug(f"Iteration: {i}.")

            token: FinalInputProtocol = tokens[i]

            if token.type == FinalTokenType.WORD and isinstance(token, FinalInputTokenWord):
                settings.logger.debug("Process `Word` token.")
                path.append(token.value)
            
            elif token.type == FinalTokenType.FLAG and isinstance(token, FinalInputTokenFlag):
                settings.logger.debug("Process `Flag` token.")
                flags[token.name] = token.value
            
            elif token.type == FinalTokenType.OPTION and isinstance(token, FinalInputTokenOption):
                settings.logger.debug("Process `Option` token.")
                options[token.name] = token.value
            
            i += 1
        
        return {
            "path": path,
            "flags": flags,
            "options": options
        }