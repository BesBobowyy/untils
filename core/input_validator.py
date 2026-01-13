from core.utils.type_aliases import InputDict
from core.utils.enums import RawTokenType, FinalTokenType, InternalState
from core.utils.constants import Strings
from core.utils.protocols import FinalInputProtocol

from core.input_token import (
    RawInputToken, FinalInputTokenWord, FinalInputTokenFlag,
    FinalInputTokenOption
)
from core.settings import Settings
from core.utils.functions import warning
from core.utils.lib_warnings import InputStructureWarning, InputValuesWarning, InputStructureError, InputValuesError
from core.commands_config import CommandsConfig
from core.command import CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode, CommandOptionNode

from typing import List, Literal, cast, Union, Dict

class InputValidator:
    """Validator class for tokenized input."""

    __slots__ = ["settings", "input_tokens", "result", "i", "debug"]

    settings: Settings
    """The settings."""
    input_tokens: List[RawInputToken]
    """The raw input tokens."""
    result: List[FinalInputProtocol]
    """The result of final input tokens."""
    i: int
    """The validation index."""
    debug: bool
    """Determines debug messages display."""

    def __init__(self, input_tokens: List[RawInputToken], debug: bool=False) -> None:
        """
        Args:
            input_tokens: The raw input tokens.
            debug: Determines debug messages display.
        """
        
        self.settings = Settings()
        self.input_tokens = input_tokens
        self.result = []
        self.i = 0
        self.debug = debug

    def warning_out_of_bounce(self) -> None:
        """Warnings out of bounce.
        
        Raises:
            InputStructureWarning: Always.

            InputStructureError: Always.
        """

        warning(
            self.settings,
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

        if self.i >= len(self.input_tokens) - offset:
            warning(
                self.settings,
                Strings.END_OF_INPUT,
                Strings.AUTO_CORRECT_WITH_ACCEPTING,
                InputStructureWarning,
                InputStructureError
            )
    
    def validate_token_word(self) -> None:
        """Validates a `Word` token."""

        token: RawInputToken = self.input_tokens[self.i]
        self.result.append(self.cast_token(FinalInputTokenWord(token.value)))
        self.i += 1
    
    def validate_token_flag(self) -> None:
        """Validates a `Flag` token."""

        value: bool = True

        invert_token: RawInputToken = self.input_tokens[self.i]
        if invert_token.type == RawTokenType.NOT:
            # Invert mark.
            if self.debug: print("Process `Not` token.")
            
            value = False
            self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
            self.i += 1
        
        name_tokens: List[RawInputToken] = self.validate_name_tokens()
        name: str = ""

        for name_token in name_tokens:
            name += name_token.value
        
        if name != "":
            # The flag's name.
            if self.debug: print("Process `Word` token for the flag's name.")
            self.result.append(self.cast_token(FinalInputTokenFlag(name, value)))
        else:
            warning(
                self.settings,
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

        if self.debug: print("Process name tokens.")

        current_token: RawInputToken = self.input_tokens[self.i]
        name_tokens: List[RawInputToken] = [current_token]

        if current_token.type == RawTokenType.STRING:
            return name_tokens
        
        if self.i == len(self.input_tokens) - 1:
            return name_tokens
        
        self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
        self.i += 1

        while (
            (self.i < len(self.input_tokens))
            and (self.input_tokens[self.i].type in (RawTokenType.WORD, RawTokenType.MINUS))
        ):
            if self.debug: print(f"Process name token: {self.input_tokens[self.i]}.")
            name_tokens.append(self.input_tokens[self.i])
            self.i += 1

        if self.debug: print(f"Processed name tokens: {name_tokens}.")

        return name_tokens

    def validate_token_option(self) -> None:
        """Validates an `Option` token."""

        name_tokens: List[RawInputToken] = self.validate_name_tokens()
        name: str = ""

        for name_token in name_tokens:
            name += name_token.value
        
        if name == "":
            warning(
                self.settings,
                Strings.OPTION_NAME_INVALID,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputStructureWarning,
                InputStructureError
            )

        self.expect_end(offset=1)  # [...][CURRENT_TOKEN][!LOOKUP!][...]
        self.i += 1

        while self.i < len(self.input_tokens) and self.input_tokens[self.i].type == RawTokenType.SPACE:
            self.i += 1

        value_tokens: List[RawInputToken] = self.validate_name_tokens()
        value: str = ""

        for value_token in value_tokens:
            value += value_token.value
        
        if value != "":
            # The option's value.
            if self.debug: print("Process `Word` or `String` token for the option's value")
            self.result.append(self.cast_token(FinalInputTokenOption(name, value)))
        else:
            warning(
                self.settings,
                Strings.OPTION_VALUE_INVALID,
                Strings.AUTO_CORRECT_WITH_SKIPPING,
                InputStructureWarning,
                InputStructureError
            )
    
    def validate_token_minus(self) -> None:
        """Validates a `Minus` token."""

        start: int = self.i

        while self.i < len(self.input_tokens) and self.input_tokens[self.i].type == RawTokenType.MINUS:
            self.i += 1
        
        count: int = self.i - start
        expected_type: Literal[FinalTokenType.FLAG, FinalTokenType.OPTION]\
            = FinalTokenType.FLAG if count == 1 else FinalTokenType.OPTION
        
        if expected_type == FinalTokenType.FLAG:
            if self.debug: print("Expected `Flag` construction.")
            self.validate_token_flag()
        elif expected_type == FinalTokenType.OPTION:
            if self.debug: print("Expected `Option` construction.")
            self.validate_token_option()
    
    def validate_input(self, settings: Settings) -> List[FinalInputProtocol]:
        """Validates a user input.
        
        Args:
            settings: The settings.

        Returns:
            The list with final validated tokens.
        """

        if self.debug: print(f"InputValidator.validate_input(input_tokens='{self.input_tokens}')")

        self.settings = settings
        self.result = []
        self.i = 0
        while self.i < len(self.input_tokens):
            if self.debug: print(f"New iteration: {self.i}.")

            prev_i: int = self.i - 1 if self.i >= 1 else 0
            next_i: int = self.i + 1 if self.i < len(self.input_tokens) - 1 else len(self.input_tokens) - 1
            if self.debug: print(
                f"[{prev_i}: {self.input_tokens[prev_i]}"\
                f" | {self.i}: {self.input_tokens[self.i]}"\
                f" | {next_i}: {self.input_tokens[next_i]}]"
            )

            token: RawInputToken = self.input_tokens[self.i]

            if token.type == RawTokenType.WORD:
                if self.debug: print("Process `Word` token.")
                self.validate_token_word()

            elif token.type == RawTokenType.MINUS:
                if self.debug: print("Process `Minus` token.")
                self.validate_token_minus()
            
            elif token.type == RawTokenType.SPACE:
                if self.debug: print("Process `Space` token.")
            
            elif token.type == RawTokenType.STRING:
                if self.debug: print("Process `String` token.")
                self.result.append(self.cast_token(FinalInputTokenWord(token.value)))
            
            else:
                if self.debug: print(f"Process unknown token: {token}.")
                warning(
                    settings,
                    Strings.UNKNOWN_TOKEN,
                    Strings.AUTO_CORRECT_WITH_SKIPPING,
                    InputStructureWarning,
                    InputStructureError
                )
            
            self.i += 1

        return self.result

class ParsedInputValidator:
    """Validator class for parsed input dict."""

    @staticmethod
    def validate_commands_path(settings: Settings, input_dict: InputDict, config: CommandsConfig) -> bool:
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
                if command.type in ("word", "fallback"):
                    command = cast(Union[CommandWordNode, CommandFallbackNode], command)
                    if (
                        (input_dict["path"][i] == command.name or command.type == "fallback")
                        or (input_dict["path"][i] in [alias.alias_name for alias in cast(CommandWordNode, command).aliases])
                    ):
                        if i == 0:
                            in_state: bool = False
                            for state_node in config.states:
                                if state_node.is_internal:
                                    if state_node.name == InternalState.BASE.value and command.name in state_node.commands:
                                        in_state = True
                                        break
                                if settings.current_state == state_node.name:
                                    in_state = command.name in state_node.commands
                                    break
                            
                            if not in_state:
                                warning(
                                    settings,
                                    Strings.COMMAND_NOT_IN_CURRENT_STATE.substitute(state=settings.current_state),
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
        
        if len(input_dict["path"]) == 0:
            validate_flags(config.commands)
            validate_options(config.commands)
            
            return all(validated_flags.values()) and all(validated_options.values())
        
        if not validate_command(config.commands, 0):
            return False
        
        validate_flags(config.commands)
        validate_options(config.commands)

        return all(validated_flags.values()) and all(validated_options.values())

    @staticmethod
    def validate_input_dict(settings: Settings, input_dict: InputDict, config: CommandsConfig) -> bool:
        """Validates input dict with current context in settings.
        
        Args:
            settings: The settings.
            input_dict: The input dictionary.
            config: The parsed commands config.

        Returns:
            `True` if the input is valid, else `False`.
        """

        return ParsedInputValidator.validate_commands_path(settings, input_dict, config)