from core.utils.type_aliases import InputDict, CommandPath, CallableCommand
from core.utils.constants import Strings

from core.commands_config import CommandsConfig
from core.settings import Settings
from core.processor import Processor
from core.input_validator import ParsedInputValidator
from core.command import CommandNode, CommandWordNode, CommandFallbackNode

from typing import Optional, List, Union, cast, Dict

class CommandSystem:
    """Core class with command config, API, processing and much more."""

    __slots__ = ["settings", "config", "route"]

    settings: Settings
    config: Optional[CommandsConfig]
    route: Dict[CommandPath, CallableCommand]

    def __init__(self, settings: Settings, config: Optional[CommandsConfig]=None) -> None:
        """
        Args:
            settings: A `Settings` object as context.
            config: A `Config` object as configuration.
        """

        self.settings = settings
        self.config = config
        self.route = {}
    
    def is_config_loaded(self) -> bool:
        """Returns a `bool` value, what determines is config loaded."""

        return self.config is not None
    
    def load_config(self, config_path: str) -> None:
        """Loads a commands config.
        
        Args:
            config_path: Real path of config file on current machine.
            debug: Determines debug messages display.
        """

        self.config = Processor.load_config(self.settings, config_path)
    
    def set_config(self, config: Optional[CommandsConfig]) -> None:
        """Sets already cached config or deletes exist.
        
        Args:
            config: Config class or it's voidness.
        """

        self.config = config
    
    def process_input(self, input_str: str) -> InputDict:
        """Processes a user input and returns `InputDict` as input representation.
        
        Args:
            input_str: Input raw string.
            debug: Determines debug messages display.
        
        Returns:
            An input representation.
        """

        return Processor.process_input(self.settings, self.config, input_str)
    
    def is_input_valid(self, input_dict: InputDict) -> bool:
        """Validates an input.
        
        Args:
            input_dict: A cached input for validation.
        
        Returns:
            `False` if an input is not valid or config not loaded. `True` if an input is valid.
        """

        if self.config is not None:
            return ParsedInputValidator.validate_input_dict(self.settings, input_dict, self.config)
        
        self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)

        return False
    
    def get_normalized_path(self, input_dict: InputDict) -> List[str]:
        """Returns original key-names in config by `path` in `input_dict`.
        
        Args:
            input_dict: A cached input for validation.
        
        Returns:
            Normalized path from original keys in config.
        """

        if self.config is None:
            self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)
            return []

        input_path: List[str] = input_dict["path"]
        commands: List[CommandNode] = self.config.commands
        result: List[str] = []

        self.settings.logger.info(Strings.LOG_CALCULATE_NORMALIZED_PATH_START)

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
        
        self.settings.logger.info(Strings.LOG_CALCULATE_NORMALIZED_PATH_END)
        
        return result
    
    def get_all_commands(self) -> List[CommandNode]:
        """Returns all commands as command nodes."""

        if self.config is None:
            self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)
            return []

        result: List[CommandNode] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                result.append(command)
        
        return result
    
    def get_all_commands_str(self) -> List[str]:
        """Returns all commands as name strings."""

        if self.config is None:
            self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)
            return []

        result: List[str] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                result.append(command.name)
        
        return result

    def get_available_commands(self) -> List[CommandNode]:
        """Returns all available commands in current state as command nodes."""

        if self.config is None:
            self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)
            return []

        result: List[CommandNode] = []

        for command in self.config.commands:
            if command.type in ("word", "fallback"):
                for state in self.config.states:
                    if command.name in state.commands:
                        result.append(command)
        
        return result

    def get_available_commands_str(self) -> List[str]:
        """Returns all available commands in current state as name strings."""

        if self.config is None:
            self.settings.logger.warning(Strings.LOG_CONFIG_NOT_LOADED)
            return []

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
        path: CommandPath,
        is_inclusive: bool=True
    ) -> bool:
        """Validates command path by input.
        
        Args:
            input_dict: A cached input for validation. Accepts `InputDict` for a path and `List[str]` only for a path.
            path: A command path, which determines all posible correct ways in path.
            is_inclusive: Always returns `False` if length of two paths are different. This argument changes validation mode: False (determines any command input from deferred path) and True (determines a single variant for command tree branching).
        
        Returns:
            `False` if input path is mispath. `True` if input path equals the deferred path.
        """

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
    
    def get_command(self, path: CommandPath) -> Optional[CallableCommand]:
        """Get a command from the command routing.
        
        Args:
            path: A command path, which determines all posible correct ways in path.
        
        Returns:
            `CallableCommand` if a function was found by a path. `None` if a function was not found.
        """

        return self.route.get(path)

    def register_command(self, path: CommandPath, func: CallableCommand) -> bool:
        """Registers a command from the command routing.
        
        Args:
            path: A command path, which determines all posible correct ways in path.
            func: A command implementation as function.
        
        Returns:
            `False` if path in the command routing. `True` if path not in the command routing and was added.
        """

        if path in self.route:
            return False
        
        self.route[path] = func
        return True
    
    def change_command(self, path: CommandPath, func: CallableCommand) -> bool:
        """Changes already registered command in the command routing.
        
        Args:
            path: A command path, which determines all posible correct ways in path.
            func: A command implementation as function.
        
        Returns:
            `False` if path not in the command routing. `True` if path in the command routing and was changed.
        """

        if path not in self.route:
            return False
        
        self.route[path] = func
        return True
    
    def unload_command(self, path: CommandPath) -> bool:
        """Removes already registered command from the command routing.
        
        Args:
            path: A command path, which determines all posible correct ways in path.
        
        Returns:
            `False` if path not in the command routing. `True` if path in the command routing and was deleted.
        """

        if path not in self.route:
            return False
        
        del self.route[path]
        return True
    
    def execute(self, input_str: str, input_dict: InputDict, normalized_path: List[str]) -> bool:
        """Executes an input string with the command routing.
        
        Args:
            input_str: An input string.
            input_dict: A cached input for validation.
            normalized_path: A command path, which determines all posible correct ways in path.
            debug: Determines debug messages display. If debug enabled and normalized path is empty, displays the message `Strings.COMMAND_NOT_WRITTEN` If debug enabled and input string is not accessed to any in the routing, displays the message `Strings.COMMAND_NOT_IMPLEMENTED`.
        
        Returns:
            `False` if a command is not written or not in the command routing. `True` if a command was called.
        """

        if len(normalized_path) == 0:
            self.settings.logger.info(Strings.COMMAND_NOT_WRITTEN)
            return False
        
        for path, func in self.route.items():
            if self.access_path(normalized_path, path, False):
                func(input_str, input_dict)
                return True
        
        self.settings.logger.warning(Strings.COMMAND_NOT_IMPLEMENTED.substitute(input_str=input_str))
        return False