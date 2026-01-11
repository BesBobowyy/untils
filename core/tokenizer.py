from core.utils.enums import RawTokenType
from core.input_token import RawInputToken

from typing import List, Literal, cast

class Tokenizer:
    """Tokenizer class."""

    __slots__ = ["input_str", "result", "i", "debug"]

    input_str: str
    result: List[RawInputToken]
    i: int
    debug: bool

    def __init__(self, input_str: str, debug: bool=False) -> None:
        self.input_str = input_str
        self.result = []
        self.i = 0
        self.debug = debug
    
    def tokenize_string(self) -> None:
        string_char: Literal['\'', '\"'] = cast(Literal['\'', '\"'], self.input_str[self.i])
        self.i += 1
        start: int = self.i

        while self.i < len(self.input_str) and self.input_str[self.i] != string_char:
            if self.input_str[self.i] == '\\' and self.input_str[self.i + 1] == string_char:
                self.i += 2
            else:
                self.i += 1
        
        string: str = self.input_str[start:self.i]
        self.result.append(RawInputToken(RawTokenType.STRING, string))
        if self.debug: print(f"String: '{string}'")
    
    def tokenize_word(self) -> None:
        start: int = self.i

        while self.i < len(self.input_str) and self.input_str[self.i].isalnum():
            self.i += 1
        
        word: str = self.input_str[start:self.i]
        self.result.append(RawInputToken(RawTokenType.WORD, word))
        if self.debug: print(f"Word: '{word}'")

    def tokenize_input(self) -> List[RawInputToken]:
        if self.debug: print(f"Tokenizer.tokenize_input(input_str='{self.input_str}')")

        self.result = []
        self.i = 0
        while self.i < len(self.input_str):
            if self.debug: print(f"Current character: {self.input_str[self.i]}.")

            if self.input_str[self.i] == ' ':
                if self.debug: print("Process Space character.")
                self.result.append(RawInputToken(RawTokenType.SPACE, ' '))

            elif self.input_str[self.i] == '-':
                if self.debug: print("Process Minus character.")
                self.result.append(RawInputToken(RawTokenType.MINUS, '-'))

            if self.input_str[self.i] == '!':
                if self.debug: print("Process Not character.")
                self.result.append(RawInputToken(RawTokenType.NOT, '!'))

            elif self.input_str[self.i] in ('\'', '\"'):
                if self.debug: print("Process `String` construction.")
                self.tokenize_string()
            
            elif self.input_str[self.i].isalnum():
                if self.debug: print("Process `Word` construction.")
                self.tokenize_word()
                continue
        
            self.i += 1
        
        return self.result