import os
import re

class JackTokenizer:
    def __init__(self, jack_input: str):
        """
        Initializes the JackTokenizer with the input Jack file or directory.

        Args:
            jack_input (str): Path to the input Jack file or directory containing Jack files.
        """
        self.current_token = ""

        if jack_input.endswith(".jack"): # input is file name
            self.jack_filenames = [jack_input]
        else: # input is dir name
            self.jack_filenames = [os.path.join(jack_input, f) for f in os.listdir(jack_input) if f.endswith(".jack")]

    def get_token(self) -> None:
        keyword_pattern = r"\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)\b"
        symbol_pattern = r"[{}()\[\].,;+\-*/&|<>=~]"
        integer_constant_pattern = r"\b(0|[1-9]\d{0,4})\b"
        string_constant_pattern = r'"[^"\n]*"'
        identifier_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        token_pattern = f"{keyword_pattern}|{symbol_pattern}|{integer_constant_pattern}|{string_constant_pattern}|{identifier_pattern}"

        for jack_filename in self.jack_filenames:
            out_filename = os.path.splitext(jack_filename)[0] + "TM.xml"
            
            with open(jack_filename, "r") as infile, open(out_filename, "w") as outfile:
                code = infile.read()
                cleaned_code = self._strip_comments(code)
                cleaned_lines = cleaned_code.splitlines()

                for line in cleaned_lines:
                    for token in re.finditer(token_pattern, line):
                        print(token.group())

    def _strip_comments(self, code):
        single_line_pattern = r'//.*?$'
        multi_line_pattern = r'/\*.*?\*/'  
        pattern = f"{single_line_pattern}|{multi_line_pattern}"
        
        return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE).strip()

    # def has_more_tokens(self) -> bool:
    #     pass

    # def advance(self) -> None:
    #     pass

    def token_type(self) -> str:
        if self.current_token in ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", 
                                  "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"):
            return "KEYWORD"
        elif self.current_token in ("{", "}", "(", ")", "[", "]", ".",  ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"):
            return "SYMBOl"
        elif self.current_token.isdigit():
            return "INT_CONST"
        elif self.current_token.startswith('"'):
            return "STRING_CONST"
        else:
            return "IDENTIFIER"


    def keyword(self) -> str:
        try:
            return self.current_token.upper()
        except:
            raise ValueError

    def symbol(self) -> str:
        return self.current_token

    def identifier(self) -> str:
        return self.current_token

    def int_val(self) -> int:
        return int(self.current_token)

    def string_val(self) -> str:
        return self.current_token