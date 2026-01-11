from core.utils.type_aliases import InputDict

from core.commands_config import CommandsConfig
from core.settings import Settings
from core.processor import Processor
from core.input_validator import ParsedInputValidator
from core.command import CommandNode

from typing import Optional, List

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