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

        #==========
        # some useful code snippets
        
        # decrement the stack pointer 
        # retrieve the value at the new top of the stack and assign it to the D register
        self.POP_STACK_TO_D = '''
@SP
M=M-1
A=M
D=M
'''

        # decrement the stack pointer
        # enable future M read to get the value at the new top of the stack
        self.GET_STACK_TO_M = '''
@SP
M=M-1
A=M
'''

        # increment the stack pointer
        # get ready for future push operations
        self.INCREMENT_STACK_POINTER = '''
@SP
M=M+1
'''

    def write_arithmetic(self, command: str, key: int) -> str:
        """
        Generates Hack assembly code for the specified arithmetic command.

        Args:
            command (str): Arithmetic command ("add", "sub", "and", "or", "neg", "not", "eq", "gt", "lt").
            outfile (TextIO): Output file to write the assembly code.
            key (int): Unique key for labeling conditional jumps.
        """

        op = self.operator_lookup[command]

        if command in ("add", "and", "or"):
            asm = f'''
{self.POP_STACK_TO_D}

{self.GET_STACK_TO_M}
M=D{op}M

{self.INCREMENT_STACK_POINTER}
            '''

        elif command == "sub":
            asm = f'''
{self.POP_STACK_TO_D}

{self.GET_STACK_TO_M}
M=M{op}D

{self.INCREMENT_STACK_POINTER}
            '''
        
        elif command in ("neg", "not"):
            asm = f'''
{self.GET_STACK_TO_M}
M={op}M

{self.INCREMENT_STACK_POINTER}
            '''
            
        else: # command in ("eq", "gt", "lt"):
            asm = f'''
{self.POP_STACK_TO_D}

{self.GET_STACK_TO_M}
D=M-D
// D now stores the difference between the previous two tops of the stack
// now we need to run conditional check

@SET_TRUE.{key}
D;{op} // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
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
{self.INCREMENT_STACK_POINTER}
            '''

        return asm

    def write_push_pop(self, command: str, segment: str, idx: int) -> str:
        # hard code command = "push" and segment = "constant" to test
        asm = f'''
@{idx}
D=A

@SP
A=M
M=D

{self.INCREMENT_STACK_POINTER}
        '''

        return asm