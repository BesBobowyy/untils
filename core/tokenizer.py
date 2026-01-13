from core.utils.enums import RawTokenType
from core.input_token import RawInputToken

from typing import List, Literal, cast

class Tokenizer:
    """Tokenizer class, which tokenize a user input."""

    __slots__ = ["_input_str", "_result", "_i", "_debug"]

    _input_str: str
    """The user input string."""
    _result: List[RawInputToken]
    """The processed raw tokens."""
    _i: int
    """Tokenize index."""
    _debug: bool
    """Is use debug output."""

    def __init__(self, input_str: str, debug: bool=False) -> None:
        """
        Args:
            input_str: The user input.
            debug: Determines debug messages display.
        """

        self._input_str = input_str
        self._result = []
        self._i = 0
        self._debug = debug
    
    def tokenize_string(self) -> None:
        """Tokenizes the `String` type."""

        string_char: Literal['\'', '\"'] = cast(Literal['\'', '\"'], self._input_str[self._i])
        self._i += 1
        start: int = self._i

        while self._i < len(self._input_str) and self._input_str[self._i] != string_char:
            if self._input_str[self._i] == '\\' and self._input_str[self._i + 1] == string_char:
                self._i += 2
            else:
                self._i += 1
        
        string: str = self._input_str[start:self._i]
        self._result.append(RawInputToken(RawTokenType.STRING, string))
        if self._debug: print(f"String: '{string}'")
    
    def tokenize_word(self) -> None:
        """Tokenizes the `Word` type."""

        start: int = self._i

        while self._i < len(self._input_str) and self._input_str[self._i].isalnum():
            self._i += 1
        
        word: str = self._input_str[start:self._i]
        self._result.append(RawInputToken(RawTokenType.WORD, word))
        if self._debug: print(f"Word: '{word}'")

    def tokenize_input(self) -> List[RawInputToken]:
        """Tokenizes the input.
        
        Returns:
            Unvalidated raw tokens.
        """

        if self._debug: print(f"Tokenizer.tokenize_input(input_str='{self._input_str}')")

        self._result = []
        self._i = 0
        while self._i < len(self._input_str):
            if self._debug: print(f"Current character: {self._input_str[self._i]}.")

            if self._input_str[self._i] == ' ':
                if self._debug: print("Process Space character.")
                self._result.append(RawInputToken(RawTokenType.SPACE, ' '))

            elif self._input_str[self._i] == '-':
                if self._debug: print("Process Minus character.")
                self._result.append(RawInputToken(RawTokenType.MINUS, '-'))

            if self._input_str[self._i] == '!':
                if self._debug: print("Process Not character.")
                self._result.append(RawInputToken(RawTokenType.NOT, '!'))

            elif self._input_str[self._i] in ('\'', '\"'):
                if self._debug: print("Process `String` construction.")
                self.tokenize_string()
            
            elif self._input_str[self._i].isalnum():
                if self._debug: print("Process `Word` construction.")
                self.tokenize_word()
                continue
        
            self._i += 1
        
        return self._result