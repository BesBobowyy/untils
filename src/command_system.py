"""command_system.py - Command system."""

# pyright: reportUnnecessaryIsInstance=false

from typing import Optional, List, Union, cast, Dict, Tuple

from src.utils.type_aliases import InputDict, CommandPath, CallableCommand, CommandHistory
from src.utils.constants import Strings

from src.commands_config import CommandsConfig
from src.settings import Settings
from src.processor import Processor
from src.input_validator import ParsedInputValidator
from src.command import CommandNode, CommandWordNode, CommandFallbackNode

class CommandSystem:
    """Core class with command config, API, processing and much more."""

    __slots__ = ["settings", "config", "route", "history"]

    settings: Settings
    config: Optional[CommandsConfig]
    route: Dict[CommandPath, CallableCommand]
    history: CommandHistory

    def __init__(
        self,
        settings: Settings,
        config: Optional[CommandsConfig]=None,
        history: Optional[CommandHistory]=None
    ) -> None:
        """
        Args:
            settings: A `Settings` object as context.
            config: A `Config` object as configuration.
            history: A command history object.
        """

        self.settings = settings
        self.config = config
        self.route = {}
        self.history = {
            "max_size": 100,
            "is_write_overflow": True,
            "notes": []
        } if history is None else history

    def is_config_loaded(self) -> bool:
        """Returns a `bool` value, what determines is config loaded."""

        return self.config is not None

    def load_config(self, config_path: str) -> None:
        """Loads a `CommandsConfig` object.
        
        Args:
            config_path: Path of config file.
        """

        self.config = Processor.load_config(self.settings, config_path)

    def set_config(self, config: Optional[CommandsConfig]) -> None:
        """Sets an already processed config or deletes exist.
        
        Args:
            config: A `Config` object or `None`.
        """

        self.config = config

    def process_input(self, input_str: str) -> InputDict:
        """Processes a user input and returns `InputDict` as input representation.
        
        Args:
            input_str: Input raw string.
        
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
                    if (
                        part == command.name
                        or part in [alias.alias_name for alias in command.aliases]
                    ):
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
            input_dict: A parsed input dict. Accepts `InputDict` for a path and `List[str]` only for a path.
            path: A command path, which determines all posible correct ways in path.
            is_inclusive: Always returns `False` if length of two paths are different. This argument changes validation mode: `False` (determines any command input from deferred path) and `True` (determines a single variant for command tree branching).
        
        Returns:
            `False` if input path is mispath. `True` if input path equals the deferred path.
        """

        if isinstance(input_dict, dict):
            input_path: List[str] = input_dict["path"]
        elif isinstance(input_dict, list):
            input_path: List[str] = input_dict
        else:
            return False

        if is_inclusive and len(path) != len(input_path):
            return False

        i: int = 0
        for part in path:
            if i >= len(input_path):
                return True

            if isinstance(part, str):
                if part in (input_path[i], "-any"):
                    i += 1
                    continue
            elif isinstance(part, (list, tuple)):
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

    def get_history(self) -> List[Tuple[str, InputDict]]:
        """Returns all notes from command history.
        
        Returns:
            List from tuples with input string and parsed input dict.
        """

        return self.history["notes"]

    def get_history_input(self) -> List[str]:
        """Returns all input strings from command history.
        
        Returns:
            List with input string.
        """

        return [note[0] for note in self.history["notes"]]

    def get_history_dict(self) -> List[InputDict]:
        """Returns all parsed input dicts from command history.
        
        Returns:
            List with parsed input dict.
        """

        return [note[1] for note in self.history["notes"]]

    def write_history(self, input_str: str, input_dict: InputDict) -> bool:
        """Writes a new note to command history.
        
        Args:
            input_str: Original input string.
            input_dict: Parsed input dict.

        Returns:
            `False` if max note count limit reached and overwrite disabled, else `True`.
        """

        if (
            len(self.history["notes"]) >= self.history["max_size"]
            and not self.history["is_write_overflow"]
        ):
            return False

        self.history["notes"].append((input_str, input_dict))
        return True

    def read_history(self, index: int) -> Tuple[str, InputDict]:
        """Returns a note by index in saved indexes.
        
        Args:
            index: Positive note index by latest. Will clamped to limits.

        Returns:
            A note from history.
        """

        return self.history["notes"][max(min(0, index), self.history["max_size"] - 1)]

    def execute(
        self,
        input_str: str,
        input_dict: InputDict,
        normalized_path: List[str],
        tracking: bool=True
    ) -> bool:
        """Executes an input string with the command routing.
        
        Args:
            input_str: An input string.
            input_dict: A cached input for validation.
            normalized_path: A command path, which determines all posible correct ways in path.
            tracking: Is save current command in history.
        
        Returns:
            `False` if a command is not written or not in the command routing. `True` if a command was called.
        """

        if tracking:
            self.write_history(input_str, input_dict)

        if len(normalized_path) == 0:
            self.settings.logger.info(Strings.COMMAND_NOT_WRITTEN)
            return False

        for path, func in self.route.items():
            if self.access_path(normalized_path, path, False):
                func(input_str, input_dict)
                return True

        self.settings.logger.warning(
            Strings.COMMAND_NOT_IMPLEMENTED.substitute(input_str=input_str)
        )
        return False
