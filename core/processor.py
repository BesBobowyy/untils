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
    def load_config(settings: Settings, file_path: str) -> CommandsConfig:
        """Loads config.
        
        Args:
            settings: The settings.
            file_path: The file path.
            debug: Determines debug messages display.
        
        Returns:
            Validated and parsed config.
        """

        settings.logger.debug(f"Load config by path: '{file_path}'.")

        ### 1. IOReader ###
        settings.logger.debug("Reading the file.")
        CONTENT: UnknownConfigType = IOReader.read_file(settings, file_path)
        settings.logger.debug(f"Content: {CONTENT}.")

        ### 2. ConfigValidator ###
        settings.logger.debug("Validating the config.")
        RAW_CONFIG: ConfigType = ConfigValidator.validate_config(settings, CONTENT)
        settings.logger.debug(f"Intermediate config: {RAW_CONFIG}.")

        ### 3. Parser ###
        settings.logger.debug("Parsing.")
        CONFIG: CommandsConfig = Parser.parse_config(RAW_CONFIG)
        settings.logger.debug(f"Parsed config: {CONFIG}.")

        return CONFIG
    
    @staticmethod
    def process_input(settings: Settings, input_str: str) -> InputDict:
        """Validates a user input.
        
        Args:
            settings: The settings.
            input_str: The user input.
            debug: Determines debug messages display.

        Returns:
            Validated and parsed input dict.
        """

        settings.logger.debug(f"Processing input string: '{input_str}'.")

        ### 1. Tokenizer ###
        settings.logger.debug("Tokenizing the input.")
        tokenizer: Tokenizer = Tokenizer(settings, input_str)
        TOKENS: List[RawInputToken] = tokenizer.tokenize_input()
        settings.logger.debug(f"Tokens: {TOKENS}.")

        ### 2. InputValidator ###
        settings.logger.debug("Validating the input.")
        input_validator: InputValidator = InputValidator(settings, TOKENS)
        VALIDATED_TOKENS: List[FinalInputProtocol] = input_validator.validate_input(settings)
        settings.logger.debug(f"Validated tokens: {VALIDATED_TOKENS}.")

        ### 3. Parser ###
        settings.logger.debug("Parsing the input.")
        PARSED_REPRESENTATION: InputDict = Parser.parse_input(settings, VALIDATED_TOKENS)
        settings.logger.debug(f"Parsed input: {PARSED_REPRESENTATION}.")

        return PARSED_REPRESENTATION