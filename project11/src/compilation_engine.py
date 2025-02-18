from jack_tokenizer import JackTokenizer, JackToken
from typing import TextIO, Literal
from symbol_table import SymbolTable, SymbolKind
from vm_writer import VMWriter
from itertools import count

Segment = Literal["this", "static", "argument", "local"]

class CompilationEngine:
    """
    Translates Jack source code into VM code.
    """
    def __init__(self, infile: TextIO, vm_out: TextIO):
        """
        Initializes the CompilationEngine with input file and VM output file.
        """
        self.infile = infile
        self.vm_out = vm_out

        self.class_name = None
        self.tokenizer = JackTokenizer(infile)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(vm_out)
        
        # these are used to differentiate between different jack if and while statements when translated to vm commands
        self.if_count = count()
        self.while_count = count()

    def compile_class(self):
        """
        Compiles a class declaration, including class variables and subroutines.
        """
        self.tokenizer.use_token() # class
        class_name_token = self.tokenizer.use_token() # class name
        self.class_name = class_name_token.get_value()
        self.tokenizer.use_token() # {
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() in ("static", "field"):
            self.compile_class_var_dec()
            self.tokenizer.buffer_token()

        while self.tokenizer.peek_token() in ("constructor", "function", "method"):
            self.compile_subroutine_dec()
            self.tokenizer.buffer_token()
        
        self.tokenizer.use_token() # }

    def compile_class_var_dec(self):
        """
        Compiles a class variable declaration (static or field).
        """
        kind_token = self.tokenizer.use_token() # static | field
        type_token = self.tokenizer.use_token() # int | char | boolean | className
        name_token = self.tokenizer.use_token() # varName
        self.symbol_table.define(name_token.get_value(), type_token.get_value(), kind_token.get_value())
        
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == ",":
            self.tokenizer.use_token() # ,
            name_token = self.tokenizer.use_token() # varName
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), kind_token.get_value())
            self.tokenizer.buffer_token()
        
        self.tokenizer.use_token() # ;

    def compile_subroutine_dec(self):
        """
        Compiles a subroutine declaration (constructor, function, method).
        """
        self.symbol_table.start_subroutine() # clear subroutine symbol table

        # subroutine dec
        kind_token = self.tokenizer.use_token() # constructor | function | method
        function_kind = kind_token.get_value()

        self.tokenizer.use_token() # void | type
        name_token = self.tokenizer.use_token() # subroutine name
        function_name = f"{self.class_name}.{name_token.get_value()}"
        
        # param list
        if function_kind == "method":
            # this is only to account for the one extra argument that the caller passes in ("this" object address)
            # since we'll never actually look up the info of this symbol based on its name, it's not important to push its name and type
            self.symbol_table.define("_", "_", "arg")
        self.tokenizer.use_token() # (
        self.compile_parameter_list() # "real" arguments
        self.tokenizer.use_token() # )

        # subroutine body
        self.tokenizer.use_token() # {
        self.compile_var_dec()
        self.vm_writer.write_function(function_name, self.symbol_table.var_count("var"))
        
        if function_kind == "constructor":
            self.vm_writer.write_push("constant", self.symbol_table.var_count("field"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)
        elif function_kind == "method":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)
        
        self.compile_statements()
        
        self.tokenizer.use_token() # }

    def compile_parameter_list(self):
        """
        Compiles a list of parameters for a subroutine.
        """
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() != ")":
            type_token = self.tokenizer.use_token() # type
            name_token = self.tokenizer.use_token() # varName
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), "arg")
            
            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self.tokenizer.use_token() # ,
                type_token = self.tokenizer.use_token() # type
                name_token = self.tokenizer.use_token() # varName
                self.symbol_table.define(name_token.get_value(), type_token.get_value(), "arg")
                
                self.tokenizer.buffer_token()

    def compile_var_dec(self):
        """
        Compiles a local variable declaration within a subroutine.
        """
        self.tokenizer.buffer_token()
        while self.tokenizer.peek_token() == "var":
            self.tokenizer.use_token() # var
            type_token = self.tokenizer.use_token() # type
            name_token = self.tokenizer.use_token() # varName
            self.symbol_table.define(name_token.get_value(), type_token.get_value(), "var")

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self.tokenizer.use_token() # ,
                name_token = self.tokenizer.use_token() # varName
                self.symbol_table.define(name_token.get_value(), type_token.get_value(), "var")
                self.tokenizer.buffer_token()
            
            self.tokenizer.use_token() # ;
            self.tokenizer.buffer_token()

    def compile_statements(self):
        """
        Compiles statements within a subroutine.
        """
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

    def compile_let(self):
        """
        Compiles a 'let' statement (variable assignment).
        """
        self.tokenizer.use_token() # let
        
        name_token = self.tokenizer.use_token() # varName
        symbol_name = name_token.get_value()
        symbol_kind = self.symbol_table.get_kind_of(symbol_name)
        symbol_idx = self.symbol_table.get_index_of(symbol_name)

        is_array = False
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "[": # evaluate the memory address of this array offset
            is_array = True
            self.vm_writer.write_push(self._kind_to_segment(symbol_kind), symbol_idx)
            self.tokenizer.use_token() # [
            self.compile_expression()
            self.tokenizer.use_token() # ]
            self.vm_writer.write_arithmetic("add")

        self.tokenizer.use_token() # =
        self.compile_expression()
        
        if is_array:
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)
        else:
            self.vm_writer.write_pop(self._kind_to_segment(symbol_kind), symbol_idx)

        self.tokenizer.use_token() # ;

    def compile_if(self):
        """
        Compiles an 'if' statement with optional 'else' block.
        """
        self.tokenizer.use_token() # if
        
        self.tokenizer.use_token() # (
        self.compile_expression()
        self.tokenizer.use_token() # )

        # get the ~ of the eval expression
        self.vm_writer.write_arithmetic("not")
        if_count = next(self.if_count)
        
        # if the ~expression is true => expression is false => go to the if-false branch (which could be an else, or nothing)
        self.vm_writer.write_if_goto(f"IF_FALSE{if_count}")
        self.tokenizer.use_token() # {
        self.compile_statements()
        self.tokenizer.use_token() # }
        self.vm_writer.write_goto(f"END_IF{if_count}")

        self.vm_writer.write_label(f"IF_FALSE{if_count}")
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "else":
            self.tokenizer.use_token() # else
            self.tokenizer.use_token() # {
            self.compile_statements()
            self.tokenizer.use_token() # }
        
        self.vm_writer.write_label(f"END_IF{if_count}")

    def compile_while(self):
        """
        Compiles a 'while' statement.
        """
        self.tokenizer.use_token() # while

        while_count = next(self.while_count)
        self.vm_writer.write_label(f"WHILE_TRUE{while_count}")

        self.tokenizer.use_token() # (
        self.compile_expression()
        self.tokenizer.use_token() # )

        # get the ~ of the eval expression
        self.vm_writer.write_arithmetic("not")
        # if the ~expression is true => expression is false => exit while loop
        self.vm_writer.write_if_goto(f"END_WHILE{while_count}")

        self.tokenizer.use_token() # {
        self.compile_statements()
        self.tokenizer.use_token() # }

        # go back to the while loop
        self.vm_writer.write_goto(f"WHILE_TRUE{while_count}")

        self.vm_writer.write_label(f"END_WHILE{while_count}")

    def compile_do(self):
        """
        Compiles a 'do' statement (subroutine call).
        """
        self.tokenizer.use_token() # do

        first_token = self.tokenizer.use_token() # subroutineName | (className | varName)
        self.compile_subroutine_call(first_token)
        self.tokenizer.use_token() # ;
        self.vm_writer.write_pop("temp", 0) # discard the unused returned value

    def compile_return(self):
        """
        Compiles a 'return' statement.
        """
        self.tokenizer.use_token() # return
        
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ";":
            self.compile_expression()
        else: # no return value
            self.vm_writer.write_push("constant", 0)
        
        self.tokenizer.use_token() # ;
        self.vm_writer.write_return()

    def compile_expression(self):
        """
        Compiles an expression.
        """
        self.compile_term() # an expression always starts with at least 1 term

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
            elif op_value == "&amp;":
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

    def compile_term(self):
        """
        Compiles a term (a part of an expression).
        """
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == "(": # (expression)
            self.tokenizer.use_token() # (
            self.compile_expression()
            self.tokenizer.use_token() # )
        elif self.tokenizer.peek_token() in ("-", "~"): # unaryOp
            op_token = self.tokenizer.use_token() # - | ~
            self.compile_term()

            op_value = op_token.get_value()
            if op_value == "-":
                self.vm_writer.write_arithmetic("neg")
            elif op_value == "~":
                self.vm_writer.write_arithmetic("not")
        else: # intConst | strConst | keywordConst | varName | varName[expression] | subroutineCall
            term_token = self.tokenizer.use_token() # intConst | strConst | keywordConst | varName
            term_type =  term_token.get_type()
            term_value = term_token.get_value()

            if term_type == "INT_CONST":
                self.vm_writer.write_push("constant", term_value)
            elif term_type == "STRING_CONST":
                # call String.new with 1 arg, the length of the strin
                self.vm_writer.write_push("constant", len(term_value))
                self.vm_writer.write_call("String.new", 1)
                for char in term_value:
                    self.vm_writer.write_push("constant", ord(char))
                    self.vm_writer.write_call("String.appendChar", 2)
            elif term_type == "KEYWORD": # true false null this
                if term_value == "true":
                    self.vm_writer.write_push("constant", "1")
                    self.vm_writer.write_arithmetic("neg")
                elif term_value == "false" or term_value == "null":
                    self.vm_writer.write_push("constant", "0")
                elif term_value == "this":
                    self.vm_writer.write_push("pointer", "0")
            else: # "IDENTIFIER"
                kind = self.symbol_table.get_kind_of(term_value)
                idx = self.symbol_table.get_index_of(term_value)
                
                self.tokenizer.buffer_token()
                if self.tokenizer.peek_token() == "[": # varName[expression]
                    self.vm_writer.write_push(self._kind_to_segment(kind), idx)
                    self.tokenizer.use_token() # [
                    self.compile_expression()
                    self.tokenizer.use_token() # ]
                    self.vm_writer.write_arithmetic("add")
                    self.vm_writer.write_pop("pointer", 1)
                    self.vm_writer.write_push("that", 0)
                elif self.tokenizer.peek_token() in ("(", "."): # function call
                    self.compile_subroutine_call(term_token)
                else: # simple varName
                    self.vm_writer.write_push(self._kind_to_segment(kind), idx)

    def compile_subroutine_call(self, first_token: JackToken):
        """
        Compiles a subroutine call, including method or function calls.
        subroutineName(expressionList)
        varName.subroutineName(expressionList)
        className.subroutineName(exprsesionList)
        
        Args:
            first_token (JackToken): the first token of this call: subroutineName | className | varName
        """
        first_symbol_name = first_token.get_value()
        is_method = False

        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() == ".":
            self.tokenizer.use_token() # .
            second_token = self.tokenizer.use_token() # subroutineName
            
            # this can potentially be the class name of an object
            # or just None if the symbol name itself is a class name
            first_symbol_type = self.symbol_table.get_type_of(first_symbol_name)

            if first_symbol_type not in (None, "int", "char", "boolean"): # method call to object of another class
                is_method = True
                first_symbol_kind = self.symbol_table.get_kind_of(first_symbol_name)
                first_symbol_idx = self.symbol_table.get_index_of(first_symbol_name)
                self.vm_writer.write_push(self._kind_to_segment(first_symbol_kind), first_symbol_idx)
                function_name = f"{first_symbol_type}.{second_token.get_value()}"
            else: # function call to another class
                function_name = f"{first_symbol_name}.{second_token.get_value()}"
        else: # method call to object of this very class
            is_method = True
            self.vm_writer.write_push("pointer", 0)
            function_name = f"{self.class_name}.{first_symbol_name}"

        self.tokenizer.use_token() # (
        num_args = self.compile_expression_list()
        self.tokenizer.use_token() # )

        if is_method:
            self.vm_writer.write_call(function_name, num_args + 1)
        else:
            self.vm_writer.write_call(function_name, num_args)

    def compile_expression_list(self) -> int:
        """
        Compiles an expression list (used in function calls).
        Returns the number of expressions in the list.
        """
        count = 0 # number of expressions separated by ,
        self.tokenizer.buffer_token()
        if self.tokenizer.peek_token() != ")":
            self.compile_expression()
            count += 1

            self.tokenizer.buffer_token()
            while self.tokenizer.peek_token() == ",":
                self.tokenizer.use_token() # ,
                self.compile_expression()
                count += 1
                self.tokenizer.buffer_token()

        return count

    def _kind_to_segment(self, kind: SymbolKind) ->  Segment:
        """
        Converts a variable kind to the corresponding VM segment.
        """
        if kind == "field":
            return "this"
        if kind == "static":
            return "static"
        if kind == "arg":
            return "argument"
        if kind == "var":
            return "local"