import re
from collections import deque
from typing import Union, Iterator, TextIO, Literal, Deque

TokenType = Literal["KEYWORD", "SYMBOL", "INT_CONST", "STRING_CONST", "IDENTIFIER"]

class JackToken:
    """
    Represents a single token in the Jack programming language.

    Attributes:
        token_type (TokenType): The type of the token.
        token_value (str): The value of the token.
    """
    def __init__(self, token_type: TokenType, token_value: str):
        self.token_type = token_type
        self.token_value = token_value

    def get_type(self) -> TokenType:
        """
        Retrieves the type of the token.
        """
        return self.token_type
    
    def get_value(self) -> str:
        """
        Retrieves the value of the token.
        """
        return self.token_value

class JackTokenizer:
    """
    Tokenizes Jack source code into JackTokens.

    Attributes:
        infile (TextIO): Input file containing Jack source code.
        buffer (Deque[JackToken]): Buffer to hold tokens temporarily.
        token_generator (Iterator[JackToken]): Generator to produce tokens.
    """
    def __init__(self, infile: TextIO):
        self.infile = infile
        self.buffer: Deque[JackToken] = deque()
        self.token_generator = self.generate_token()

    def use_token(self) -> JackToken:
        """
        Retrieves and pops the next token from the buffer if there's any.
        Else retrieves it directly from the generator.
        """
        if self.buffer:
            return self.buffer.popleft()
        
        return next(self.token_generator)

    def buffer_token(self) -> None:
        """
        Adds the next token from the generator to the buffer, if there's any left.
        """
        try:
            self.buffer.append(next(self.token_generator))
        except:
            pass

    def peek_token(self, idx: int = 0) -> None:
        """
        Views the value of a token in the buffer without consuming it.
        """
        return self.buffer[idx].get_value()

    def generate_token(self) -> Iterator[JackToken]:
        """
        Generates tokens from the Jack source code.
        """
        keyword_pattern = r"\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)\b"
        symbol_pattern = r"[{}()\[\].,;+\-*/&|<>=~]"
        integer_constant_pattern = r"\b(0|[1-9]\d{0,4})\b"
        string_constant_pattern = r'"([^"\n]*)"'
        identifier_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        token_pattern = f"{keyword_pattern}|{symbol_pattern}|{integer_constant_pattern}|{string_constant_pattern}|{identifier_pattern}"
        
        code = self.infile.read()
        cleaned_code = self._strip_comments(code)
        cleaned_lines = cleaned_code.splitlines()

        for line in cleaned_lines:
            for token in re.finditer(token_pattern, line):
                token_str = token.group()
                token_type = self.get_token_type(token_str)
                token_value = self.get_token_value(token_str, token_type)
                yield JackToken(token_type, token_value)

    def _strip_comments(self, code: str) -> str:
        """
        Removes comments from the Jack source code.
        """
        single_line_pattern = r'//.*?$'
        multi_line_pattern = r'/\*.*?\*/'  
        pattern = f"{single_line_pattern}|{multi_line_pattern}"
        
        return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE).strip()

    def get_token_type(self, token: str) -> TokenType:
        """
        Determines the type of a given token.
        """
        if token in ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", 
                                  "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"):
            return "KEYWORD"
        elif token in ("{", "}", "(", ")", "[", "]", ".",  ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"):
            return "SYMBOL"
        elif token.isdigit():
            return "INT_CONST"
        elif token.startswith('"'):
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def get_token_value(self, token: str, token_type: TokenType) -> Union[str, int]:
        """
        Interprets the value of a given token based on its type.
        """
        if token_type == "KEYWORD":
            return self._keyword_val(token)
        elif token_type == "SYMBOL":
            return self._symbol_val(token)
        elif token_type == "INT_CONST":
            return self._int_val(token)
        elif token_type == "STRING_CONST":
            return self._string_val(token)
        elif token_type == "IDENTIFIER":
            return self._identifier_val(token)

    def _keyword_val(self, token: str) -> str:
        """
        Interprets the value of a keyword token.
        """
        return token

    def _symbol_val(self, token: str) -> str:
        """
        Interprets the value of a symbol token.
        """
        if token == "<":
            return "&lt;"
        elif token == ">":
            return "&gt;"
        elif token == '"':
            return "&quot;"
        elif token == "&":
            return "&amp;"
        else:
            return token

    def _int_val(self, token: str) -> int:
        """
        Interprets the value of an integer constant token.
        """
        return int(token)

    def _string_val(self, token: str) -> str:
        """
        Interprets the value of a string constant token.
        """
        return token.strip('"')
    
    def _identifier_val(self, token: str) -> str:
        """
        Interprets the value of an identifier token.
        """
        return token