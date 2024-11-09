from jack_tokenizer import JackTokenizer
from typing import TextIO

class CompilationEngine:
    def __init__(self, infile: TextIO, outfile: TextIO):
        self.infile = infile
        self.outfile = outfile
        self.tokenizer = JackTokenizer(infile)

    def compile_class(self):
        self.outfile.write("<class>\n")

        self._write_tag(self.tokenizer.use_token()) # class
        self._write_tag(self.tokenizer.use_token()) # class name
        self._write_tag(self.tokenizer.use_token()) # {
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("static", "field"):
            self.outfile.write("<classVarDec>\n")
            self.compile_class_var_dec()
            self.outfile.write("</classVarDec>\n")
            self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() in ("constructor", "function", "method"):
            self.outfile.write("<subroutineDec>\n")
            self.compile_subroutine_dec()
            self.outfile.write("</subroutineDec>\n")
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # }

        self.outfile.write("</class>")

    def compile_class_var_dec(self):
        self._write_tag(self.tokenizer.use_token()) # static | field
        self._write_tag(self.tokenizer.use_token()) # type: int | char | boolean | className
        self._write_tag(self.tokenizer.use_token()) # var name
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == ",":
            self._write_tag(self.tokenizer.use_token()) # ,
            self._write_tag(self.tokenizer.use_token()) # varName
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # ;

    def compile_subroutine_dec(self):
        self._write_tag(self.tokenizer.use_token()) # constructor | function | method
        self._write_tag(self.tokenizer.use_token()) # void | type
        self._write_tag(self.tokenizer.use_token()) # subroutine name
        
        self._write_tag(self.tokenizer.use_token()) # (
        self.outfile.write("<parameterList>\n")
        self.compile_parameter_list()
        self.outfile.write("</parameterList>\n")
        self._write_tag(self.tokenizer.use_token()) # )

        self.outfile.write("<subroutineBody>\n")
        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_var_dec()
        # self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }
        self.outfile.write("</subroutineBody>\n")

    def compile_parameter_list(self):
        self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() != ")":
            self._write_tag(self.tokenizer.use_token()) # type
            self._write_tag(self.tokenizer.use_token()) # varName
            
            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                self._write_tag(self.tokenizer.use_token()) # type
                self._write_tag(self.tokenizer.use_token()) # varName
                self.tokenizer.buffer_token()

    def compile_var_dec(self):
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == "var":
            self.outfile.write("<varDec>\n")
            self._write_tag(self.tokenizer.use_token()) # var
            self._write_tag(self.tokenizer.use_token()) # type
            self._write_tag(self.tokenizer.use_token()) # varName

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                self._write_tag(self.tokenizer.use_token()) # varName
                self.tokenizer.buffer_token()
            
            self._write_tag(self.tokenizer.use_token()) # ;
            self.outfile.write("</varDec>\n")
            
            self.tokenizer.buffer_token()

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass
    
    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

    def _write_tag(self, token) -> str:
        token_type, token_value = token

        match token_type:
            case "KEYWORD":
                token_tag = "keyword"
            case "SYMBOL":
                token_tag = "symbol"
            case "INT_CONST":
                token_tag = "integerConstant"
            case "STRING_CONST":
                token_tag = "stringConstant"
            case _:
                token_tag = "identifier"
        
        self.outfile.write(f"<{token_tag}> ")
        self.outfile.write(f"{token_value}")
        self.outfile.write(f" </{token_tag}>\n")