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
            self.compile_class_var_dec()
            self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() in ("constructor", "function", "method"):
            self.compile_subroutine_dec()
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # }

        self.outfile.write("</class>\n")

    def compile_class_var_dec(self):
        self.outfile.write("<classVarDec>\n")

        self._write_tag(self.tokenizer.use_token()) # static | field
        self._write_tag(self.tokenizer.use_token()) # type: int | char | boolean | className
        self._write_tag(self.tokenizer.use_token()) # var name
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == ",":
            self._write_tag(self.tokenizer.use_token()) # ,
            self._write_tag(self.tokenizer.use_token()) # varName
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # ;
        self.outfile.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        self.outfile.write("<subroutineDec>\n")

        self._write_tag(self.tokenizer.use_token()) # constructor | function | method
        self._write_tag(self.tokenizer.use_token()) # void | type
        self._write_tag(self.tokenizer.use_token()) # subroutine name
        
        self._write_tag(self.tokenizer.use_token()) # (
        self.outfile.write("<parameterList>\n")
        self.compile_parameter_list()
        self.outfile.write("</parameterList>\n")
        self._write_tag(self.tokenizer.use_token()) # )

        self.compile_subroutine_body()
        self.outfile.write("</subroutineDec>\n")

    def compile_subroutine_body(self):
        self.outfile.write("<subroutineBody>\n")
        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_var_dec()
        self.compile_statements()
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
        self.outfile.write("<statements>\n")
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("let", "if", "while", "do", "return"):
            match self.tokenizer.peek_token():
                case "let":
                    self.compile_let()
                case "if":
                    self.compile_if()
                case "while":
                    self.compile_while()
                case "do":
                    self.compile_do()
                case "return":
                    self.compile_return()
            
            self.tokenizer.buffer_token()
        
        self.outfile.write("</statements>\n")

    def compile_let(self):
        self.outfile.write("<letStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # let
        self._write_tag(self.tokenizer.use_token()) # varName

        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "[":
            self._write_tag(self.tokenizer.use_token()) # [
            self.compile_expression()
            self._write_tag(self.tokenizer.use_token()) # ]

        self._write_tag(self.tokenizer.use_token()) # =
        self.compile_expression()

        self._write_tag(self.tokenizer.use_token()) # ;
        self.outfile.write("</letStatement>\n")

    def compile_if(self):
        self.outfile.write("<ifStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # if
        
        self._write_tag(self.tokenizer.use_token()) # (
        self.compile_expression()
        self._write_tag(self.tokenizer.use_token()) # )

        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }

        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "else":
            self._write_tag(self.tokenizer.use_token()) # else
            self._write_tag(self.tokenizer.use_token()) # {
            self.compile_statements()
            self._write_tag(self.tokenizer.use_token()) # }
        
        self.outfile.write("</ifStatement>\n")

    def compile_while(self):
        self.outfile.write("<whileStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # while

        self._write_tag(self.tokenizer.use_token()) # (
        self.compile_expression()
        self._write_tag(self.tokenizer.use_token()) # )

        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }

        self.outfile.write("</whileStatement>\n")

    def compile_do(self):
        self.outfile.write("<doStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # do

        self._write_tag(self.tokenizer.use_token()) # subroutineName | (className | varName)
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == ".":
            self._write_tag(self.tokenizer.use_token()) # .
            self._write_tag(self.tokenizer.use_token()) # subroutineName

        self._write_tag(self.tokenizer.use_token()) # (
        self.compile_expression_list()
        self._write_tag(self.tokenizer.use_token()) # )

        self._write_tag(self.tokenizer.use_token()) # ;
        self.outfile.write("</doStatement>\n")

    def compile_return(self):
        self.outfile.write("<returnStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # return
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ";":
            self.compile_expression()
        
        self._write_tag(self.tokenizer.use_token()) # ;
        self.outfile.write("</returnStatement>\n")

    def compile_expression(self):
        self.outfile.write("<expression>\n")
        
        self.compile_term()

        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("+", "-", "*", "/", "&", "|", "<", ">", "="):
            self._write_tag(self.tokenizer.use_token()) # op
            self.compile_term()
            self.tokenizer.buffer_token()

        self.outfile.write("</expression>\n")

    def compile_term(self):
        self.outfile.write("<term>\n")

        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "(": # (expression)
            self._write_tag(self.tokenizer.use_token()) # (
            self.compile_expression()
            self._write_tag(self.tokenizer.use_token()) # )
        elif self.tokenizer.peek_token() in ("-", "~"): # unaryOp term
            self._write_tag(self.tokenizer.use_token()) # - | ~
            self.compile_term()
        else:
            self._write_tag(self.tokenizer.use_token()) # intConst | strConst | keywordConst | varName
            
            self.tokenizer.buffer_token()
            if self.tokenizer.peek_token() == "[":
                self._write_tag(self.tokenizer.use_token()) # [
                self.compile_expression()
                self._write_tag(self.tokenizer.use_token()) # ]
            elif self.tokenizer.peek_token() == "(":
                self._write_tag(self.tokenizer.use_token()) # (
                self.compile_expression_list()
                self._write_tag(self.tokenizer.use_token()) # )
            elif self.tokenizer.peek_token() == ".":
                self._write_tag(self.tokenizer.use_token()) # .
                self._write_tag(self.tokenizer.use_token()) # subroutineName
                self._write_tag(self.tokenizer.use_token()) # (
                self.compile_expression_list()
                self._write_tag(self.tokenizer.use_token()) # )

        self.outfile.write("</term>\n")

    def compile_expression_list(self):
        self.outfile.write("<expressionList>\n")
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ")":
            self.compile_expression()

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                self.compile_expression()
                self.tokenizer.buffer_token()

        self.outfile.write("</expressionList>\n")

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