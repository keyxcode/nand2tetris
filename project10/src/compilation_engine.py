from jack_tokenizer import JackTokenizer
from typing import TextIO

class CompilationEngine:
    def __init__(self, infile: TextIO, outfile: TextIO):
        self.infile = infile
        self.outfile = outfile
        self.token_generator = JackTokenizer(infile).get_token()

    def compile_class(self):
        for _ in range(20):
            token_type, token_value = next(self.token_generator)
            self.outfile.write(token_type + token_value + "\n")

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

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