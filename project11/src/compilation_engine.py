from jack_tokenizer import JackTokenizer, JackToken
from typing import TextIO, Literal
from symbol_table import SymbolTable, SymbolKind
from vm_writer import VMWriter
from itertools import count

Segment = Literal["this", "static", "argument", "local"]

class CompilationEngine:
    def __init__(self, infile: TextIO, xml_out: TextIO, vm_out: TextIO):
        self.infile = infile
        self.xml_out = xml_out
        self.vm_out = vm_out

        self.class_name = None
        self.tokenizer = JackTokenizer(infile)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(vm_out)

        self.if_count = count()
        self.while_count = count()

    def compile_class(self):
        self.xml_out.write("<class>\n")

        self._write_tag(self.tokenizer.use_token()) # class
        class_name_token = self.tokenizer.use_token()
        self.class_name = class_name_token.get_value()
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
        self.symbol_table.define(name_token.get_value(), type_token.get_value(), kind_token.get_value())
        self._write_tag(name_token) # varName
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == ",":
            self._write_tag(self.tokenizer.use_token()) # ,
            name_token = self.tokenizer.use_token()
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), kind_token.get_value())
            self._write_tag(name_token) # varName
            self.tokenizer.buffer_token()
        
        self._write_tag(self.tokenizer.use_token()) # ;
        self.xml_out.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()

        self.xml_out.write("<subroutineDec>\n")

        function_kind_token = self.tokenizer.use_token()
        if function_kind_token.get_value() == "method":
            self.symbol_table.define("this", self.class_name, "arg")

        self._write_tag(function_kind_token) # constructor | function | method
        self._write_tag(self.tokenizer.use_token()) # void | type
        name_token = self.tokenizer.use_token()
        function_name = f"{self.class_name}.{name_token.get_value()}"
        self._write_tag(name_token) # subroutine name
        
        self._write_tag(self.tokenizer.use_token()) # (
        self.xml_out.write("<parameterList>\n")
        self.compile_parameter_list()
        self.xml_out.write("</parameterList>\n")
        self._write_tag(self.tokenizer.use_token()) # )

        self.xml_out.write("<subroutineBody>\n")
        self._write_tag(self.tokenizer.use_token()) # {
        self.compile_var_dec()
        self.vm_writer.write_function(function_name, self.symbol_table.var_count("var"))

        self.compile_statements()
        self._write_tag(self.tokenizer.use_token()) # }
        self.xml_out.write("</subroutineBody>\n")

        self.xml_out.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() != ")":
            type_token = self.tokenizer.use_token()
            self._write_tag(type_token) # type
            name_token = self.tokenizer.use_token()
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), "arg")
            self._write_tag(name_token) # varName
            
            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                type_token = self.tokenizer.use_token()
                self._write_tag(type_token) # type
                name_token = self.tokenizer.use_token()
                self.symbol_table.define(name_token.get_value(), type_token.get_value(), "arg")
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
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), "var")
            self._write_tag(name_token) # varName

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                name_token = self.tokenizer.use_token()
                self.symbol_table.define(name_token.get_value(), type_token.get_value(), "var")
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
        self.tokenizer.use_token() # let
        name_token = self.tokenizer.use_token() # varName

        # TODO: var is an array
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "[":
            self.tokenizer.use_token() # [
            self.compile_expression()
            self.tokenizer.use_token() # ]

        self.tokenizer.use_token() # =
        self.compile_expression()

        name_token_value = name_token.get_value()
        kind = self.symbol_table.get_kind_of(name_token_value)
        idx = self.symbol_table.get_index_of(name_token_value)

        self.tokenizer.use_token() # ;

    def compile_if(self):
        self.tokenizer.use_token() # if
        
        self.tokenizer.use_token() # (
        self.compile_expression()
        self.tokenizer.use_token() # )

        # get the ~ of the eval expression
        self.vm_writer.write_arithmetic("not")
        if_count = next(self.if_count)
        
        # if the ~expression is true => expression is false => go to the if-false branch (which could be an else, or nothing)
        self.vm_writer.write_if_goto(f"IF-FALSE{if_count}")
        self.tokenizer.use_token() # {
        self.compile_statements()
        self.tokenizer.use_token() # }
        self.vm_writer.write_goto(f"END-IF{if_count}")

        self.vm_writer.write_label(f"IF-FALSE{if_count}")
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "else":
            self.tokenizer.use_token() # else
            self.tokenizer.use_token() # {
            self.compile_statements()
            self.tokenizer.use_token() # }
        
        self.vm_writer.write_label(f"END-IF{if_count}")

    def compile_while(self):
        self.tokenizer.use_token() # while

        self.vm_writer.write_label(f"WHILE-TRUE{while_count}")

        self.tokenizer.use_token() # (
        self.compile_expression()
        self.tokenizer.use_token() # )

        # get the ~ of the eval expression
        self.vm_writer.write_arithmetic("not")
        while_count = next(self.while_count)
        # if the ~expression is true => expression is false => exit while loop
        self.vm_writer.write_if_goto(f"END-WHILE{while_count}")

        self.tokenizer.use_token() # {
        self.compile_statements()
        self.tokenizer.use_token() # }

        # go back to the while loop
        self.vm_writer.write_goto(f"WHILE-TRUE{while_count}")

        self.vm_writer.write_label(f"END-WHILE{while_count}")

    def compile_do(self):
        self.tokenizer.use_token() # do

        first_name_token = self.tokenizer.use_token() # subroutineName | (className | varName)
        function_name = first_name_token.get_value()
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == ".":
            self.tokenizer.use_token() # .
            second_name_token = self.tokenizer.use_token() # subroutineName
            function_name += f".{second_name_token.get_value()}"

        self.tokenizer.use_token() # (
        num_args = self.compile_expression_list()
        self.tokenizer.use_token() # )

        self.tokenizer.use_token() # ;

        self.vm_writer.write_call(function_name, num_args)
        self.vm_writer.write_pop("temp", 0) # discard the unused returned value

    def compile_return(self):
        self.tokenizer.use_token() # return
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ";":
            self.compile_expression()
        else: # no return value
            self.vm_writer.write_push("constant", 0)
            self.vm_writer.write_return()
        
        self.tokenizer.use_token() # ;

    def compile_expression(self):
        self.xml_out.write("<expression>\n")
        # an expression always starts with at least 1 term
        self.compile_term()

        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="):
            op_token = self.tokenizer.use_token() # op
            self.compile_term()

            op_value = op_token.get_value()
            if op_value == "+":
                self.vm_writer.write_arithmetic("add")
            elif op_value == "-":
                self.vm_writer.write_arithmetic("sub")
            elif op_value == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            elif op_value == "/":
                self.vm_writer.write_call("Math.divide", 2)
            elif op_value == "&amp":
                self.vm_writer.write_arithmetic("and")
            elif op_value == "|":
                self.vm_writer.write_arithmetic("or")
            elif op_value == "&lt;":
                self.vm_writer.write_arithmetic("lt")
            elif op_value == "&gt;":
                self.vm_writer.write_arithmetic("gt")
            elif op_value == "=":
                self.vm_writer.write_arithmetic("eq")
            
            self.tokenizer.buffer_token()

        self.xml_out.write("</expression>\n")

    def compile_term(self):
        self.xml_out.write("<term>\n")

        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "(": # (expression)
            self.tokenizer.use_token() # (
            self.compile_expression()
            self.tokenizer.use_token() # )
        elif self.tokenizer.peek_token() in ("-", "~"): # unaryOp term
            op_token = self.tokenizer.use_token() # - | ~
            self.compile_term()

            op_value = op_token.get_value()
            if op_value == "-":
                self.vm_writer.write_arithmetic("neg")
            elif op_value == "~":
                self.vm_writer.write_arithmetic("not")
        else:
            term_token = self.tokenizer.use_token() # intConst | strConst | keywordConst | varName
            # TODO: fix this hard-coded intConst
            term_type =  term_token.get_type()
            term_value = term_token.get_value()
            if term_type == "INT_CONST":
                self.vm_writer.write_push("constant", term_value)
            elif term_type == "STRING_CONST":
                # call String.new with 1 arg, the length of the strin
                self.vm_writer.write_push("constant", len(term_value))
                self.vm_writer.write_call("String.new", 1)
                for char in term_value:
                    self.vm_writer.write_push("constant", term_value)
                    self.vm_writer.write_call("String.appendChar", ord(char))
            elif term_type == "KEYWORD":
                if term_value == "true":
                    self.vm_writer.write_push("constant", "-1")
                elif term_value == "false" or term_value == "null":
                    self.vm_writer.write_push("constant", "0")
            elif term_type == "IDENTIFIER":
                kind = self.symbol_table.get_kind_of(term_value)
                idx = self.symbol_table.get_index_of(term_value)
                self.vm_writer.write_push(self._kind_to_segment(kind), idx)
            
            # TODO: if term is array, object or function call
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

    def compile_expression_list(self) -> int:
        '''Return number of expressions in the expression list'''
        self.xml_out.write("<expressionList>\n")
        
        count = 0
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ")":
            self.compile_expression()
            count += 1

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self._write_tag(self.tokenizer.use_token()) # ,
                self.compile_expression()
                count += 1
                self.tokenizer.buffer_token()

        self.xml_out.write("</expressionList>\n")
        return count

    def _write_tag(self, token: JackToken) -> str:
        token_type = token.get_type()
        token_value = token.get_value()

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

    def _kind_to_segment(self, kind: SymbolKind) ->  Segment:
        if kind == "field":
            return "this"
        if kind == "static":
            return "static"
        if kind == "arg":
            return "argument"
        if kind == "var":
            return "local"
        