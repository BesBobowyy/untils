"""*mplib* - Is light-weight library for console games or small utils to process user input as commands and describe structure with config."""

# pyright: reportUnusedImport=false
# ^^^^^^^ (Public imports.)

from src import utils

from src.command_system import CommandSystem
from src.command import (
    AliasNode, CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode,
    CommandOptionNode, StateNode
)
from src.commands_config import CommandsConfig
from src.config_validator import ConfigValidator
from src.factories import CommandNodeFactory
from src.input_token import (
    RawInputToken, FinalInputTokenWord, FinalInputTokenFlag, FinalInputTokenOption
)
from src.input_validator import InputValidator, ParsedInputValidator
from src.ioreader import IOReader
from src.iovalidator import IOValidator
from src.parser import Parser
from src.processor import Processor
from src.settings import Settings
from src.tokenizer import Tokenizer
