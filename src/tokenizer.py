from src.utils.enums import RawTokenType
from src.input_token import RawInputToken

from src.settings import Settings

from typing import List, Literal, cast

class Tokenizer:
    """Tokenizer class, which tokenizes user input."""

    __slots__ = ["_settings", "_input_str", "_result", "_i"]

    _settings: Settings
    """The settings."""
    _input_str: str
    """The user input string."""
    _result: List[RawInputToken]
    """The processed raw tokens."""
    _i: int
    """Tokenize index."""

    def __init__(self, settings: Settings, input_str: str) -> None:
        """
        Args:
            input_str: The user input.
            debug: Determines debug messages display.
        """

        self._settings = settings
        self._input_str = input_str
        self._result = []
        self._i = 0
    
    def tokenize_string(self) -> None:
        """Tokenizes the `String` type."""

        string_char: Literal['\'', '\"'] = cast(Literal['\'', '\"'], self._input_str[self._i])
        self._i += 1
        string: str = ""

        while self._i < len(self._input_str) and self._input_str[self._i] != string_char:
            if self._input_str[self._i] == '\\':
                if self._input_str[self._i + 1] in ('\'', '\"'):
                    string += self._input_str[self._i + 1]
                elif self._input_str[self._i + 1] == '\\':
                    string += self._input_str[self._i]
                
                self._i += 1
            else:
                string += self._input_str[self._i]

            self._i += 1
        
        self._result.append(RawInputToken(RawTokenType.STRING, string))
        self._settings.logger.debug(f"String: '{string}'")
    
    def tokenize_word(self) -> None:
        """Tokenizes the `Word` type."""

        start: int = self._i

        while self._i < len(self._input_str) and self._input_str[self._i].isalnum():
            self._i += 1
        
        word: str = self._input_str[start:self._i]
        self._result.append(RawInputToken(RawTokenType.WORD, word))
        self._settings.logger.debug(f"Word: '{word}'")

    def tokenize_input(self) -> List[RawInputToken]:
        """Tokenizes the input.
        
        Returns:
            Unvalidated raw tokens.
        """

        self._settings.logger.debug(f"Tokenizer.tokenize_input(input_str='{self._input_str}')")

        self._result = []
        self._i = 0
        while self._i < len(self._input_str):
            self._settings.logger.debug(f"Current character: {self._input_str[self._i]}.")

            if self._input_str[self._i] == ' ':
                self._settings.logger.debug("Process Space character.")
                self._result.append(RawInputToken(RawTokenType.SPACE, ' '))

            elif self._input_str[self._i] == '-':
                self._settings.logger.debug("Process Minus character.")
                self._result.append(RawInputToken(RawTokenType.MINUS, '-'))

            if self._input_str[self._i] == '!':
                self._settings.logger.debug("Process Not character.")
                self._result.append(RawInputToken(RawTokenType.NOT, '!'))

            elif self._input_str[self._i] in ('\'', '\"'):
                self._settings.logger.debug("Process `String` construction.")
                self.tokenize_string()
            
            elif self._input_str[self._i].isalnum():
                self._settings.logger.debug("Process `Word` construction.")
                self.tokenize_word()
                continue
        
            self._i += 1
        
        return self._result