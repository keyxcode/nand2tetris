import os, sys
from typing import Dict, List, TextIO


def get_command_type(command: str) -> str:
    command = command.lower()

    if command.startswith("push"):
        return "C_PUSH"
    if command.startswith("pop"):
        return "C_POP"
    if command.startswith(("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")):
        return "C_ARITHMETIC"
    
    # dummy fall back. in the future we'll support more command types
    return ""

def write_arithmetic(command: str, outfile: TextIO, key: int) -> None:
    # need to support:
    # add, sub, and, or
    # neg, not
    # eq, gt, lt,

    command_lookups = {
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

    # binary arithmetic and logical
    if command in ("add", "and", "or"):
        command = command_lookups[command]

        asm = f'''
@SP
M=M-1
A=M
D=M

@SP
M=M-1
A=M
M=D{command}M

@SP
M=M+1
        '''

    elif command in ("sub"):
        command = command_lookups[command]

        asm = f'''
@SP
M=M-1
A=M
D=M

@SP
M=M-1
A=M
M=M{command}D

@SP
M=M+1
        '''
    
    # unary arithmetic and logical
    elif command in ("neg", "not"):
        command = command_lookups[command]

        asm = f'''
@SP
M=M-1
A=M
M={command}M

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
    else: # command in ("eq", "gt", "lt"):
        command = command_lookups[command]

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
D;{command}
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

    outfile.write(asm)

def write_push_pop(command: str, segment: str, idx: int, outfile: TextIO) -> None:
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <vm-dir-name>")
        sys.exit(1)

    # assume that the vm code dir is a subdir of ../vm/
    # and the output assembly will be in ../bin/
    vm_dirname = os.path.join("..", "vm", sys.argv[1])
    out_filename = os.path.join("..", "asm", os.path.splitext(sys.argv[1])[0] + ".asm")
    
    vm_filenames = [os.path.join("..", "vm", vm_dirname, f) for f in os.listdir(vm_dirname) if f.endswith(".vm")]
    for vm_filename in vm_filenames:
        with open(vm_filename, "r") as infile, open(out_filename, "w") as outfile:
            for i, line in enumerate(infile):
                # only parse valid code line
                if not line.startswith("//") and line.strip():
                    command_type = get_command_type(line)
                    components = line.split()
                    if command_type == "C_ARITHMETIC":
                        arg1 = components[0]
                        write_arithmetic(arg1, outfile, i)
                    elif command_type != "C_RETURN":
                        arg1 = components[1]
                        if command_type in ("C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"):
                            arg2 = components[2]
                        write_push_pop(components[0], arg1, arg2, outfile)


if __name__ == "__main__":
    main()