"""processor.py - `Processor` class for universal pipe-lines."""

from typing import List, Optional

from untils.utils.type_aliases import UnknownConfigType, ConfigType, InputDict
from untils.utils.protocols import FinalInputProtocol

from untils.ioreader import IOReader
from untils.config_validator import ConfigValidator
from untils.parser import Parser
from untils.commands_config import CommandsConfig
from untils.settings import Settings
from untils.input_token import RawInputToken
from untils.tokenizer import Tokenizer
from untils.input_validator import InputValidator

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
        content: UnknownConfigType = IOReader.read_file(settings, file_path)
        settings.logger.debug(f"Content: {content}.")

        ### 2. ConfigValidator ###
        settings.logger.debug("Validating the config.")
        raw_config: ConfigType = ConfigValidator.validate_config(settings, content)
        settings.logger.debug(f"Intermediate config: {raw_config}.")

        ### 3. Parser ###
        settings.logger.debug("Parsing.")
        config: CommandsConfig = Parser.parse_config(raw_config)
        settings.logger.debug(f"Parsed config: {config}.")

        return config

    @staticmethod
    def process_input(
        settings: Settings,
        config: Optional[CommandsConfig],
        input_str: str
    ) -> InputDict:
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
        tokens: List[RawInputToken] = tokenizer.tokenize_input()
        settings.logger.debug(f"Tokens: {tokens}.")

        ### 2. InputValidator ###
        settings.logger.debug("Validating the input.")
        input_validator: InputValidator = InputValidator(settings, config, tokens)
        validated_tokens: List[FinalInputProtocol] = input_validator.validate_input(settings)
        settings.logger.debug(f"Validated tokens: {validated_tokens}.")

        ### 3. Parser ###
        settings.logger.debug("Parsing the input.")
        parsed_representation: InputDict = Parser.parse_input(settings, validated_tokens)
        settings.logger.debug(f"Parsed input: {parsed_representation}.")

        return parsed_representation
