from typing import TextIO

class CodeWriter:
    def __init__(self):
        self.operator_lookup = {
            "add": "+",
            "sub": "-",
            "and": "&",
            "or": "|",
            "neg": "-",
            "not": "!",
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT"
        }

    def write_arithmetic(self, command: str, outfile: TextIO, key: int) -> None:
        op = self.operator_lookup[command]

        if command in ("add", "and", "or"):
            asm = f'''
@SP
M=M-1
A=M
D=M

@SP
M=M-1
A=M
M=D{op}M

@SP
M=M+1
            '''

        elif command in ("sub"):
            asm = f'''
@SP
M=M-1
A=M
D=M

@SP
M=M-1
A=M
M=M{op}D

@SP
M=M+1
            '''
        
        # unary arithmetic and logical
        elif command in ("neg", "not"):
            asm = f'''
@SP
M=M-1
A=M
M={op}M

@SP
M=M+1
            '''
            
        else: # command in ("eq", "gt", "lt"):
            asm = f'''
@SP
M=M-1
A=M
D=M

@SP
M=M-1
A=M
D=M-D

@SET_TRUE.{key}
D;{op}
@SP
A=M
M=0
@END.{key}
0;JMP

(SET_TRUE.{key})
@SP
A=M
M=-1

(END.{key})
@SP
M=M+1
            '''
        # top of the stack now is the difference between a - b
        # now we need to run conditional check

        # if op is eq:
        #     if diff == 0: push true
        #     else: push false
        # if op is gt:
        #     if diff > 0: push true
        #     else: push false
        # if op is lt:
        #     if diff < 0: push true
        #     else: push false

        # simplified:
        # if op is eq, use JEQ
        # if op is gt, use JGT
        # if op is lt, use JLT
        # then if diff op 0: push true
        # else: push false
        outfile.write(asm)

    def write_push_pop(self, command: str, segment: str, idx: int, outfile: TextIO) -> None:
        # hard code command = "push" and segment = "constant" to test
        asm = f'''
@{idx}
D=A

@SP
A=M
M=D

@SP
M=M+1
        '''
        outfile.write(asm)