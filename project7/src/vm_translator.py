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

def write_arithmetic(command: str, outfile: TextIO) -> None:
    # hard code arithmetic = "+" to test
    asm = f'''
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M
        A=A+1
    '''
    print(asm)
    outfile.write(asm + "\n")

def write_push_pop(command: str, segment: str, idx: int, outfile: TextIO) -> None:
    # hard code command = "push" and segment = "constant" to test
    asm = f'''
        @{idx}
        D=A
        @SP
        A=M
        M=D
        D=A+1
        @SP
        M=D
    '''
    print(asm)
    outfile.write(asm + "\n")

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
            for line in infile:
                # only parse valid code line
                if not line.startswith("//") and line.strip():
                    command_type = get_command_type(line)
                    components = line.split()
                    if command_type == "C_ARITHMETIC":
                        arg1 = components[0]
                        write_arithmetic(arg1, outfile)
                    elif command_type != "C_RETURN":
                        arg1 = components[1]
                        if command_type in ("C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"):
                            arg2 = components[2]
                        write_push_pop(components[0], arg1, arg2, outfile)


if __name__ == "__main__":
    main()