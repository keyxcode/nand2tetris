import re
from typing import Union, Tuple, Iterator
from typing import TextIO

class JackTokenizer:
    def __init__(self, infile: TextIO):
        self.infile = infile

    def get_token(self) -> Iterator[Tuple[Union[int, str], str]]:
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
                yield (token_type, token_value)

                # token_tag = ""            
                # match token_type:
                #     case "KEYWORD":
                #         token_tag = "keyword"
                #     case "SYMBOL":
                #         token_tag = "symbol"
                #     case "INT_CONST":
                #         token_tag = "integerConstant"
                #     case "STRING_CONST":
                #         token_tag = "stringConstant"
                #     case _:
                #         token_tag = "identifier"
                
                
                # print(token_value, token_type)
                # outfile.write(f"<{token_tag}> ")
                # outfile.write(f"{token_value}")
                # outfile.write(f" </{token_tag}>\n")
        
        # outfile.write("</tokens>\n")

    def _strip_comments(self, code):
        single_line_pattern = r'//.*?$'
        multi_line_pattern = r'/\*.*?\*/'  
        pattern = f"{single_line_pattern}|{multi_line_pattern}"
        
        return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE).strip()

    # def has_more_tokens(self) -> bool:
    #     pass

    # def advance(self) -> None:
    #     pass

    def get_token_type(self, token: str) -> str:
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

    def get_token_value(self, token: str, token_type: str) -> Union[str, int]:
        match token_type:
            case "KEYWORD":
                return self._keyword_val(token)
            case "SYMBOL":
                return self._symbol_val(token)
            case "INT_CONST":
                return self._int_val(token)
            case "STRING_CONST":
                return self._string_val(token)
            case "IDENTIFIER":
                return self._identifier_val(token)

    def _keyword_val(self, token: str) -> str:
        return token

    def _symbol_val(self, token: str) -> str:
        match token:
            case "<":
                return "&lt;"
            case ">":
                return "&gt;"
            case '"':
                return "&quot;"
            case "&":
                return "&amp;"
            case _:
                return token

    def _int_val(self, token: str) -> int:
        return int(token)

    def _string_val(self, token: str) -> str:
        return token.strip('"')
    
    def _identifier_val(self, token: str) -> str:
        return token