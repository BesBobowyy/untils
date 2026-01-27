"""input_validator.py - Input validations."""

from typing import List, Literal, cast, Union, Dict, Optional

from src.utils.type_aliases import InputDict
from src.utils.enums import RawTokenType, FinalTokenType, InternalState
from src.utils.constants import Strings
from src.utils.protocols import FinalInputProtocol

from src.input_token import (
    RawInputToken, FinalInputTokenWord, FinalInputTokenFlag,
    FinalInputTokenOption
)
from src.settings import Settings
from src.utils.functions import warning
from src.utils.lib_warnings import (
    InputStructureWarning, InputValuesWarning, InputStructureError, InputValuesError
)
from src.commands_config import CommandsConfig
from src.command import (
    CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode, CommandOptionNode
)

class InputValidator:
    """Validator class for tokenized input."""

    __slots__ = ["_settings", "_config", "_input_tokens", "_result", "_i"]

    _settings: Settings
    """The settings."""
    _config: Optional[CommandsConfig]
    """The commands config."""
    _input_tokens: List[RawInputToken]
    """The raw input tokens."""
    _result: List[FinalInputProtocol]
    """The result of final input tokens."""
    _i: int
    """The validation index."""

    def __init__(
        self,
        settings: Settings,
        config: Optional[CommandsConfig],
        input_tokens: List[RawInputToken]
    ) -> None:
        """
        Args:
            input_tokens: The raw input tokens.
            config: The validated and parsed commands config.
            debug: Determines debug messages display.
        """

        self._settings = settings
        self._config = config
        self._input_tokens = input_tokens
        self._result = []
        self._i = 0

    def warning_out_of_bounce(self) -> None:
        """Warnings out of bounce.
        
        Raises:
            InputStructureWarning: Always.

            InputStructureError: Always.
        """

        warning(
            self._settings,
            Strings.END_OF_INPUT,
            Strings.AUTO_CORRECT_WITH_REMOVING,
            InputStructureWarning,
            InputStructureError
        )

    def cast_token(
        self,
        token_object: Union[FinalInputTokenWord, FinalInputTokenFlag, FinalInputTokenOption]
    ) -> FinalInputProtocol:
        """Casts a token to the `FinalInputProtocol`.
        
        Args:
            token_object: The token.
        
        Returns:
            The casted token.
        """

        return cast(FinalInputProtocol, token_object)

    def expect_end(self, offset: int=1) -> None:
        """Expects an end by offset.
        
        Args:
            offset: The number greater than 0, which defines an index offset, that cannot be out of bounce.
        
        Raises:
            InputStructureWarning: If the offset out of bounce.

            InputStructureError: If the offset out of bounce.
        """

        if self._i >= len(self._input_tokens) - offset:
            warning(
                self._settings,
                Strings.END_OF_INPUT,
                Strings.AUTO_CORRECT_WITH_ACCEPTING,
                InputStructureWarning,
                InputStructureError
            )

    def validate_token_word(self) -> None:
        """Validates a `Word` token."""

        token: RawInputToken = self._input_tokens[self._i]
        self._result.append(self.cast_token(FinalInputTokenWord(token.value)))
        self._i += 1

    def validate_token_flag(self) -> None:
        """Validates a `Flag` token."""

        value: bool = True

        invert_token: RawInputToken = self._input_tokens[self._i]
        if invert_token.type == RawTokenType.NOT:
            # Invert mark.
            self._settings.logger.debug("Process `Not` token.")

            value = False
            self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
            self._i += 1

        name_tokens: List[RawInputToken] = self.validate_name_tokens()
        name: str = ""

        for name_token in name_tokens:
            name += name_token.value

        if name != "":
            # The flag's name.
            self._settings.logger.debug("Process `Word` token for the flag's name.")
            self._result.append(self.cast_token(FinalInputTokenFlag(name, value)))
        else:
            warning(
                self._settings,
                Strings.EXPECTED_SYNTAX_FLAG,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputStructureWarning,
                InputStructureError
            )

    def validate_name_tokens(self) -> List[RawInputToken]:
        """Validates a row of tokens with type `Word` and `String` without spaces as name.
        
        Returns:
            The list of name tokens.
        """

        self._settings.logger.debug("Process name tokens.")

        current_token: RawInputToken = self._input_tokens[self._i]
        name_tokens: List[RawInputToken] = [current_token]

        if current_token.type == RawTokenType.STRING:
            return name_tokens

        if self._i == len(self._input_tokens) - 1:
            return name_tokens

        self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
        self._i += 1

        while (
            (self._i < len(self._input_tokens))
            and (self._input_tokens[self._i].type in (RawTokenType.WORD, RawTokenType.MINUS))
        ):
            self._settings.logger.debug(f"Process name token: {self._input_tokens[self._i]}.")
            name_tokens.append(self._input_tokens[self._i])
            self._i += 1

        self._settings.logger.debug(f"Processed name tokens: {name_tokens}.")

        return name_tokens

    def validate_token_option(self) -> None:
        """Validates an `Option` token."""

        name_tokens: List[RawInputToken] = self.validate_name_tokens()
        name: str = ""

        for name_token in name_tokens:
            name += name_token.value

        if name == "":
            warning(
                self._settings,
                Strings.OPTION_NAME_INVALID,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputStructureWarning,
                InputStructureError
            )

        self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
        self._i += 1

        while (
            self._i < len(self._input_tokens)
            and self._input_tokens[self._i].type == RawTokenType.SPACE
        ):
            self._i += 1

        value_tokens: List[RawInputToken] = self.validate_name_tokens()
        value: str = ""

        for value_token in value_tokens:
            value += value_token.value

        if value != "":
            # The option's value.
            self._settings.logger.debug("Process `Word` or `String` token for the option's value")
            self._result.append(self.cast_token(FinalInputTokenOption(name, value)))
        else:
            warning(
                self._settings,
                Strings.OPTION_VALUE_INVALID,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputStructureWarning,
                InputStructureError
            )

    def validate_token_minus(self) -> None:
        """Validates a `Minus` token."""

        start: int = self._i

        while (
            self._i < len(self._input_tokens)
            and self._input_tokens[self._i].type == RawTokenType.MINUS
        ):
            self._i += 1

        count: int = self._i - start
        expected_type: Literal[FinalTokenType.FLAG, FinalTokenType.OPTION]\
            = FinalTokenType.FLAG if count == 1 else FinalTokenType.OPTION

        if expected_type == FinalTokenType.FLAG:
            self._settings.logger.debug("Expected `Flag` construction.")
            self.validate_token_flag()
        elif expected_type == FinalTokenType.OPTION:
            self._settings.logger.debug("Expected `Option` construction.")
            self.validate_token_option()

    def validate_fallback_defaults(self) -> None:
        """Validates `Fallback` commands with defaults in path if they not written."""

        result: List[FinalInputProtocol] = []
        commands: List[CommandNode] = self._config.commands if self._config is not None else []

        found: bool = False
        for part in self._result:
            # Copying.
            found = False
            for node in commands:
                if node.type == "word":
                    node = cast(CommandWordNode, node)

                    if not (
                        node.name == part.value
                        or part.value in [alias.alias_name for alias in node.aliases]
                    ):
                        continue
                elif node.type == "fallback":
                    node = cast(CommandFallbackNode, node)
                else:
                    continue

                result.append(part)
                commands = node.children
                found = True
                break

            if not found:
                # Invalid path.
                return

        while commands != []:
            # Searching `Fallback`s.
            found = False

            for node in commands:
                if node.type == "fallback":
                    node = cast(CommandFallbackNode, node)
                    result.append(self.cast_token(FinalInputTokenWord(str(node.default))))
                    commands = node.children
                    found = True
                    break

            if not found:
                # Invalid path.
                return

        self._result = result

    def validate_input(self, settings: Settings) -> List[FinalInputProtocol]:
        """Validates a user input.
        
        Args:
            settings: The settings.

        Returns:
            The list with final validated tokens.
        """

        self._settings.logger.debug(
            f"InputValidator.validate_input(input_tokens='{self._input_tokens}')"
        )

        self._settings = settings
        self._result = []
        self._i = 0

        while self._i < len(self._input_tokens):
            self._settings.logger.debug(f"New iteration: {self._i}.")

            token: RawInputToken = self._input_tokens[self._i]

            if token.type == RawTokenType.WORD:
                self._settings.logger.debug("Process `Word` token.")
                self.validate_token_word()

            elif token.type == RawTokenType.MINUS:
                self._settings.logger.debug("Process `Minus` token.")
                self.validate_token_minus()

            elif token.type == RawTokenType.SPACE:
                self._settings.logger.debug("Process `Space` token.")

            elif token.type == RawTokenType.STRING:
                self._settings.logger.debug("Process `String` token.")
                self._result.append(self.cast_token(FinalInputTokenWord(token.value)))

            else:
                self._settings.logger.debug(f"Process unknown token: {token}.")
                warning(
                    settings,
                    Strings.UNKNOWN_TOKEN,
                    Strings.AUTO_CORRECT_WITH_SKIPPING,
                    InputStructureWarning,
                    InputStructureError
                )

            self._i += 1

        self.validate_fallback_defaults()

        return self._result

class ParsedInputValidator:
    """Validator class for parsed input dict."""

    @staticmethod
    def validate_commands_path(
        settings: Settings,
        input_dict: InputDict,
        config: CommandsConfig
    ) -> bool:
        """Validates a commands path, flags and options.
        
        Args:
            settings: The settings.
            input_dict: The parsed input dictionary.
            config: The parsed commands config.

        Returns:
            `True` if commands path, flags and options is valid, else `False`.

        Raises:
            InputValuesWarning: If the first command is not written in current state in the settings or path cannot be accessed to the input path.

            InputValuesError: If the first command is not written in current state in the settings or path cannot be accessed to the input path.
        """

        flag_keys: List[str] = list(input_dict["flags"].keys())
        option_keys: List[str] = list(input_dict["options"].keys())
        validated_flags: Dict[str, bool] = {n: False for n in flag_keys}
        validated_options: Dict[str, bool] = {n: False for n in option_keys}

        def validate_flags(children: List[CommandNode]) -> None:
            """Validates the flags.
            
            Args:
                children: The commands.
            """

            for command in children:
                if command.type == "flag":
                    command = cast(CommandFlagNode, command)
                    validated_flags[command.name] = True
                    for alias in command.aliases:
                        validated_flags[alias.alias_name] = True

        def validate_options(children: List[CommandNode]) -> None:
            """Validates the options.
            
            Args:
                children: The commands.
            """

            for command in children:
                if command.type == "option":
                    command = cast(CommandOptionNode, command)
                    validated_options[command.name] = True
                    for alias in command.aliases:
                        validated_options[alias.alias_name] = True

        def validate_command(children: List[CommandNode], i: int) -> bool:
            """Validates a command recursively.
            
            Args:
                children: The commands.
                i: Current path index.

            Returns:
                `False` if command not in current state (i == 0 -> First command) or has not children, else `True`.

            Raises:
                InputValuesWarning: If the first command is not written in current state in the settings or no commands in children in path.

                InputValuesError: If the first command is not written in current state in the settings or no commands in children in path.
            """

            for command in children:
                if command.type not in ("word", "fallback"):
                    # Type filtration for positioned commands.
                    continue

                command = cast(Union[CommandWordNode, CommandFallbackNode], command)

                if command.type == "word":
                    # Conditions:
                    # 1. `command.type == "word"`` -> Shall equals with original command key or with alias.
                    # 2. `command.type == "fallback"` -> None (accepts any word).
                    command = cast(CommandWordNode, command)

                    if input_dict["path"][i] == command.name:
                        # Continue current iteration.
                        pass
                    elif input_dict["path"][i] not in [
                         alias.alias_name for alias in command.aliases
                    ]:
                        # Next iteration.
                        continue

                if i == 0:
                    # First iteration must has root command.
                    in_state: bool = False
                    for state_node in config.states:
                        if state_node.is_internal:
                            if (
                                state_node.name == InternalState.BASE.value
                                and command.name in state_node.commands
                            ):
                                # First state in `__base__` state, which defines any current state.
                                in_state = True
                                break
                        if settings.current_state == state_node.name:
                            # Command defined in current state.
                            in_state = command.name in state_node.commands
                            break

                    if not in_state:
                        # First iteration not in states.
                        warning(
                            settings,
                            Strings.COMMAND_NOT_IN_CURRENT_STATE.substitute(
                                state=settings.current_state
                            ),
                            Strings.AUTO_CORRECT_WITH_SKIPPING,
                            InputValuesWarning,
                            InputValuesError
                        )
                        return False

                validate_flags(command.children)
                validate_options(command.children)

                if i < len(input_dict["path"]) - 1:
                    validate_command(command.children, i + 1)

                return True

            warning(
                settings,
                Strings.INPUT_PATH_INVALID.substitute(name=input_dict["path"][i]),
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputValuesWarning,
                InputValuesError
            )

            return False

        if input_dict["path"] == []:
            # Current path is empty.
            validate_flags(config.commands)
            validate_options(config.commands)

            return all(validated_flags.values()) and all(validated_options.values())

        if not validate_command(config.commands, 0):
            return False

        validate_flags(config.commands)
        validate_options(config.commands)

        return all(validated_flags.values()) and all(validated_options.values())

    @staticmethod
    def validate_input_dict(
        settings: Settings,
        input_dict: InputDict,
        config: CommandsConfig
    ) -> bool:
        """Validates input dict with current context in settings.
        
        Args:
            settings: The settings.
            input_dict: The input dictionary.
            config: The parsed commands config.

        Returns:
            `True` if the input is valid, else `False`.
        """

        return ParsedInputValidator.validate_commands_path(settings, input_dict, config)
