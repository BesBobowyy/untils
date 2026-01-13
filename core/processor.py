from core.utils.type_aliases import UnknownConfigType, ConfigType, InputDict
from core.utils.protocols import FinalInputProtocol

from core.ioreader import IOReader
from core.config_validator import ConfigValidator
from core.parser import Parser
from core.commands_config import CommandsConfig
from core.settings import Settings
from core.input_token import RawInputToken
from core.tokenizer import Tokenizer
from core.input_validator import InputValidator

from typing import List

class Processor:
    """Processor class for config processing."""

    @staticmethod
    def load_config(settings: Settings, file_path: str, debug: bool=False) -> CommandsConfig:
        """Loads config.
        
        Args:
            settings: The settings.
            file_path: The file path.
            debug: Determines debug messages display.
        
        Returns:
            Validated and parsed config.
        """

        if debug: print(f"--- Load config by path: {repr(file_path)} ---")

        ### 1. IOReader ###
        if debug: print("--- Reading the file ---")
        CONTENT: UnknownConfigType = IOReader.read_file(settings, file_path)
        if debug: print(f"Content: {CONTENT}")

        ### 2. ConfigValidator ###
        if debug: print("--- Validating the config ---")
        RAW_CONFIG: ConfigType = ConfigValidator.validate_config(settings, CONTENT)
        if debug: print(f"Intermediate config: {RAW_CONFIG}")

        ### 3. Parser ###
        if debug: print("--- Parsing ---")
        CONFIG: CommandsConfig = Parser.parse_config(RAW_CONFIG)
        if debug: print("Parsed config: <TODO>")

        return CONFIG
    
    @staticmethod
    def process_input(settings: Settings, input_str: str, debug: bool=False) -> InputDict:
        """Validates a user input.
        
        Args:
            settings: The settings.
            input_str: The user input.
            debug: Determines debug messages display.

        Returns:
            Validated and parsed input dict.
        """

        if debug: print(f"--- Processing input string: '{input_str}' ---")

        ### 1. Tokenizer ###
        if debug: print("--- Tokenizing the input ---")
        tokenizer: Tokenizer = Tokenizer(input_str, debug)
        TOKENS: List[RawInputToken] = tokenizer.tokenize_input()
        if debug: print(f"Tokens: {TOKENS}")

        ### 2. InputValidator ###
        if debug: print("--- Validating the input ---")
        input_validator: InputValidator = InputValidator(TOKENS, debug)
        VALIDATED_TOKENS: List[FinalInputProtocol] = input_validator.validate_input(settings)
        if debug: print(f"Validated tokens: {VALIDATED_TOKENS}")

        ### 3. Parser ###
        if debug: print("--- Parsing the input ---")
        PARSED_REPRESENTATION: InputDict = Parser.parse_input(VALIDATED_TOKENS, debug)
        if debug: print(f"Parsed input: {PARSED_REPRESENTATION}")

        return PARSED_REPRESENTATION