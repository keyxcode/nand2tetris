from jack_tokenizer import JackTokenizer, TokenTuple
from typing import TextIO
from symbol_table import SymbolTable

class CompilationEngine:
    def __init__(self, infile: TextIO, xml_out: TextIO, vm_out: TextIO):
        self.infile = infile
        self.xml_out = xml_out
        self.vm_out = vm_out

        self.class_name = None
        self.tokenizer = JackTokenizer(infile)
        self.symbol_table = SymbolTable()

    def compile_class(self):
        self.xml_out.write("<class>\n")

        self._write_tag(self.tokenizer.use_token()) # class
        class_name_token = self.tokenizer.use_token()
        self.class_name = class_name_token[1]
        self._write_tag(class_name_token) # class name
        self._write_tag(self.tokenizer.use_token()) # {
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("static", "field"):
            self.compile_class_var_dec()
            self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() in ("constructor", "function", "method"):
            self.compile_subroutine_dec()
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # }

        self.xml_out.write("</class>\n")

    def compile_class_var_dec(self):
        self.xml_out.write("<classVarDec>\n")

        kind_token = self.tokenizer.use_token()
        self._write_tag(kind_token) # static | field
        type_token = self.tokenizer.use_token()
        self._write_tag(type_token) # type: int | char | boolean | className
        name_token = self.tokenizer.use_token()
        self.symbol_table.define(name_token[1], type_token[1], kind_token[1])
        self._write_tag(name_token) # varName
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == ",":
            self._write_tag(self.tokenizer.use_token()) # ,
            name_token = self.tokenizer.use_token()
            self.symbol_table.define(name_token[1], type_token[1], kind_token[1])
            self._write_tag(name_token) # varName
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # ;
        self.xml_out.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()

        self.xml_out.write("<subroutineDec>\n")

        function_kind_token = self.tokenizer.use_token()
        if function_kind_token[1] == "method":
            self.symbol_table.define("this", self.class_name, "arg")

        self._write_tag(function_kind_token) # constructor | function | method
        self._write_tag(self.tokenizer.use_token()) # void | type
        self._write_tag(self.tokenizer.use_token()) # subroutine name
        
        self._write_tag(self.tokenizer.use_token()) # (
        self.xml_out.write("<parameterList>\n")
        self.compile_parameter_list()
        self.xml_out.write("</parameterList>\n")
        self._write_tag(self.tokenizer.use_token()) # )

        self.compile_subroutine_body()
        self.xml_out.write("</subroutineDec>\n")

    def compile_subroutine_body(self):
        self.xml_out.write("<subroutineBody>\n")
        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_var_dec()
        self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }
        self.xml_out.write("</subroutineBody>\n")

    def compile_parameter_list(self):
        self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() != ")":
            type_token = self.tokenizer.use_token()
            self._write_tag(type_token) # type
            name_token = self.tokenizer.use_token()
            self.symbol_table.define(name_token[1], type_token[1], "arg")
            self._write_tag(name_token) # varName
            
            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                type_token = self.tokenizer.use_token()
                self._write_tag(type_token) # type
                name_token = self.tokenizer.use_token()
                self.symbol_table.define(name_token[1], type_token[1], "arg")
                self._write_tag(name_token) # varName
                self.tokenizer.buffer_token()

    def compile_var_dec(self):
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == "var":
            self.xml_out.write("<varDec>\n")
            self._write_tag(self.tokenizer.use_token()) # var
            type_token = self.tokenizer.use_token()
            self._write_tag(type_token) # type
            name_token = self.tokenizer.use_token()
            self.symbol_table.define(name_token[1], type_token[1], "var")
            self._write_tag(name_token) # varName

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                name_token = self.tokenizer.use_token()
                self.symbol_table.define(name_token[1], type_token[1], "var")
                self._write_tag(name_token) # varName
                self.tokenizer.buffer_token()
            
            self._write_tag(self.tokenizer.use_token()) # ;
            self.xml_out.write("</varDec>\n")

            self.tokenizer.buffer_token()

    def compile_statements(self): 
        self.xml_out.write("<statements>\n")
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("let", "if", "while", "do", "return"):
            peek_token = self.tokenizer.peek_token()

            if peek_token == "let":
                self.compile_let()
            elif peek_token == "if":
                self.compile_if()
            elif peek_token == "while":
                self.compile_while()
            elif peek_token == "do":
                self.compile_do()
            elif peek_token == "return":
                self.compile_return()
            
            self.tokenizer.buffer_token()
        
        self.xml_out.write("</statements>\n")

    def compile_let(self):
        self.xml_out.write("<letStatement>\n")
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
        self.xml_out.write("</letStatement>\n")

    def compile_if(self):
        self.xml_out.write("<ifStatement>\n")
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
        
        self.xml_out.write("</ifStatement>\n")

    def compile_while(self):
        self.xml_out.write("<whileStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # while

        self._write_tag(self.tokenizer.use_token()) # (
        self.compile_expression()
        self._write_tag(self.tokenizer.use_token()) # )

        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }

        self.xml_out.write("</whileStatement>\n")

    def compile_do(self):
        self.xml_out.write("<doStatement>\n")
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
        self.xml_out.write("</doStatement>\n")

    def compile_return(self):
        self.xml_out.write("<returnStatement>\n")
        self._write_tag(self.tokenizer.use_token()) # return
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ";":
            self.compile_expression()
        
        self._write_tag(self.tokenizer.use_token()) # ;
        self.xml_out.write("</returnStatement>\n")

    def compile_expression(self):
        self.xml_out.write("<expression>\n")
        
        self.compile_term()

        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="):
            self._write_tag(self.tokenizer.use_token()) # op
            self.compile_term()
            self.tokenizer.buffer_token()

        self.xml_out.write("</expression>\n")

    def compile_term(self):
        self.xml_out.write("<term>\n")

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
            if self.tokenizer.peek_token() == "[": # varName[expression]
                self._write_tag(self.tokenizer.use_token()) # [
                self.compile_expression()
                self._write_tag(self.tokenizer.use_token()) # ]
            elif self.tokenizer.peek_token() == "(": # subroutineName(expressionList)
                self._write_tag(self.tokenizer.use_token()) # (
                self.compile_expression_list()
                self._write_tag(self.tokenizer.use_token()) # )
            elif self.tokenizer.peek_token() == ".": # (className | varName).subroutineName(expressionList)
                self._write_tag(self.tokenizer.use_token()) # .
                self._write_tag(self.tokenizer.use_token()) # subroutineName
                self._write_tag(self.tokenizer.use_token()) # (
                self.compile_expression_list()
                self._write_tag(self.tokenizer.use_token()) # )

        self.xml_out.write("</term>\n")

    def compile_expression_list(self):
        self.xml_out.write("<expressionList>\n")
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ")":
            self.compile_expression()

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                self.compile_expression()
                self.tokenizer.buffer_token()

        self.xml_out.write("</expressionList>\n")

    def _write_tag(self, token: TokenTuple) -> str:
        token_type, token_value = token

        if token_type == "KEYWORD":
            token_tag = "keyword"
        elif token_type == "SYMBOL":
            token_tag = "symbol"
        elif token_type == "INT_CONST":
            token_tag = "integerConstant"
        elif token_type == "STRING_CONST":
            token_tag = "stringConstant"
        else:
            token_tag = "identifier"
        
        if token_tag == "identifier" and self.symbol_table.get_kind_of(token_value):
            attributes = f"kind={self.symbol_table.get_kind_of(token_value)} type={self.symbol_table.get_type_of(token_value)} idx={self.symbol_table.get_index_of(token_value)}"
            self.xml_out.write(f"<{token_tag} {attributes}> ")
        else:
            self.xml_out.write(f"<{token_tag}> ")
        self.xml_out.write(f"{token_value}")
        self.xml_out.write(f" </{token_tag}>\n")