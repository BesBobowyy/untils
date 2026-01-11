from core.utils.type_aliases import InputDict

from core.commands_config import CommandsConfig
from core.settings import Settings
from core.processor import Processor
from core.input_validator import ParsedInputValidator
from core.command import CommandNode, CommandWordNode, CommandFallbackNode

from typing import Optional, List, Union, Tuple, cast

class CommandSystem:
    """Core class with command config, API, processing and much more."""

    __slots__ = ["settings", "config"]

    settings: Settings
    config: Optional[CommandsConfig]

    def __init__(self, settings: Optional[Settings]=None, config: Optional[CommandsConfig]=None) -> None:
        self.settings = settings or Settings()
        self.config = config
    
    def is_config_loaded(self) -> bool:
        return self.config is not None
    
    def load_config(self, config_path: str, debug: bool=False) -> None:
        self.config = Processor.load_config(self.settings, config_path, debug)
    
    def set_config(self, config: Optional[CommandsConfig]) -> None:
        """Set already processed config."""

        self.config = config
    
    def process_input(self, input_str: str, debug: bool=False) -> InputDict:
        return Processor.process_input(self.settings, input_str, debug)
    
    def is_input_valid(self, input_dict: InputDict) -> bool:
        if self.config is not None:
            return ParsedInputValidator.validate_input_dict(self.settings, input_dict, self.config)
        return False
    
    def get_normalized_path(self, input_dict: InputDict) -> List[str]:
        if self.config is None:
            return []

        input_path: List[str] = input_dict["path"]
        commands: List[CommandNode] = self.config.commands
        result: List[str] = []

        for part in input_path:
            for command in commands:
                if command.type == "word":
                    command = cast(CommandWordNode, command)
                    if part == command.name or part in [alias.alias_name for alias in command.aliases]:
                        result.append(command.name)
                        commands = command.children
                        break
                elif command.type == "fallback":
                    command = cast(CommandFallbackNode, command)
                    result.append(command.name)
                    commands = command.children
                    break
        
        return result
    
    def get_all_commands(self) -> List[CommandNode]:
        if self.config is None: return []

        result: List[CommandNode] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                result.append(command)
        
        return result
    
    def get_all_commands_str(self) -> List[str]:
        if self.config is None: return []

        result: List[str] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                result.append(command.name)
        
        return result

    def get_available_commands(self) -> List[CommandNode]:
        if self.config is None: return []

        result: List[CommandNode] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                for state in self.config.states:
                    if command.name in state.commands:
                        result.append(command)
        
        return result

    def get_available_commands_str(self) -> List[str]:
        if self.config is None: return []

        result: List[str] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                for state in self.config.states:
                    if command.name in state.commands:
                        result.append(command.name)
        
        return result
    
    def access_path(
        self,
        input_dict: Union[InputDict, List[str]],
        path: List[Union[str, List[str], Tuple[str, ...]]],
        is_inclusive: bool=True
    ) -> bool:
        if isinstance(input_dict, dict):
            input_path: List[str] = input_dict["path"]
        elif type(input_dict) == list:
            input_path: List[str] = input_dict
        else:
            return False
        
        if is_inclusive and len(path) != len(input_path):
            return False
        
        i: int = 0
        for part in path:
            if i >= len(input_path):
                return True

            if type(part) == str:
                if input_path[i] == part or part == "-any":
                    i += 1
                    continue
            elif type(part) in (list, tuple):
                if input_path[i] in part:
                    i += 1
                    continue
            return False
        return True