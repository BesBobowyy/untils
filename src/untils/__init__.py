"""*untils* - Is light-weight library for console games or small utils to process user input as commands and describe structure with config."""

# pyright: reportUnusedImport=false
# ^^^^^^^ (Public imports.)

from untils import utils

from untils.command_system import CommandSystem
from untils.command import (
    AliasNode, CommandNode, CommandWordNode, CommandFallbackNode, CommandFlagNode,
    CommandOptionNode, StateNode
)
from untils.commands_config import CommandsConfig
from untils.config_validator import ConfigValidator
from untils.factories import CommandNodeFactory
from untils.input_token import (
    RawInputToken, FinalInputTokenWord, FinalInputTokenFlag, FinalInputTokenOption
)
from untils.input_validator import InputValidator, ParsedInputValidator
from untils.ioreader import IOReader
from untils.iovalidator import IOValidator
from untils.parser import Parser
from untils.processor import Processor
from untils.settings import Settings
from untils.tokenizer import Tokenizer

__version__ = "1.0.1"
__author__ = "BesBobowyy"
