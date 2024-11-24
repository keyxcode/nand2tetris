import re
from collections import deque
from typing import Union, Iterator, TextIO, Literal, Deque

TokenType = Literal["KEYWORD", "SYMBOL", "INT_CONST", "STRING_CONST", "IDENTIFIER"]

class JackToken:
    def __init__(self, token_type: TokenType, token_value: str):
        self.token_type = token_type
        self.token_value = token_value

    def get_type(self) -> TokenType:
        return self.token_type
    
    def get_value(self) -> str:
        return self.token_value

class JackTokenizer:
    def __init__(self, infile: TextIO):
        self.infile = infile
        self.buffer: Deque[JackToken] = deque()
        self.token_generator = self.generate_token()

    def use_token(self) -> JackToken:
        # pop the first token in the buffer if there's any
        # if buffer is empty, use the generator next
        if self.buffer:
            return self.buffer.popleft()
        
        return next(self.token_generator)

    def buffer_token(self) -> None:
        # call generator next and store it in the token queue
        try:
            self.buffer.append(next(self.token_generator))
        except:
            pass

    def peek_token(self, idx: int = 0) -> None:
        # view token value in queue at idx, if there's any
        return self.buffer[idx].get_value()

    def generate_token(self) -> Iterator[JackToken]:
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

    def _strip_comments(self, code):
        single_line_pattern = r'//.*?$'
        multi_line_pattern = r'/\*.*?\*/'  
        pattern = f"{single_line_pattern}|{multi_line_pattern}"
        
        return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE).strip()

    def get_token_type(self, token: str) -> TokenType:
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
        return token

    def _symbol_val(self, token: str) -> str:
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
        return int(token)

    def _string_val(self, token: str) -> str:
        return token.strip('"')
    
    def _identifier_val(self, token: str) -> str:
        return token