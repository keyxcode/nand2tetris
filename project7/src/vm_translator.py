import os, sys
from code_writer import CodeWriter

class VMTranslator:
    def __init__(self, vm_filenames, out_filename):
        self.code_writer = CodeWriter()
        self.vm_filenames = vm_filenames
        self.out_filename = out_filename


    def get_command_type(self, command: str) -> str:
        command = command.lower()

        if command.startswith("push"):
            return "C_PUSH"
        if command.startswith("pop"):
            return "C_POP"
        if command.startswith(("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")):
            return "C_ARITHMETIC"
        
        # dummy fall back. in the future we'll support more command types
        return ""

    def parse(self) -> None:
        for vm_filename in self.vm_filenames:
            with open(vm_filename, "r") as infile, open(self.out_filename, "w") as outfile:
                for key, line in enumerate(infile): # use line num as the key for code writer methods
                    if line.startswith("//") or not line.strip():
                        continue # ignore empty line/ comment

                    command_type = self.get_command_type(line)
                    command_components = line.split()
                    
                    if command_type == "C_ARITHMETIC": # only 1 component
                        asm = self.code_writer.write_arithmetic(command_components[0], key)
                    elif command_type != "C_RETURN": 
                        # assume only ("C_PUSH", "C_POP") e.g. push local 0
                        # will have to refactor this in the future to support function and call commands
                        command, segment, idx = command_components
                        asm = self.code_writer.write_push_pop(command, segment, idx, key)
                    
                    outfile.write(asm)

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <vm-dir-name>")
        sys.exit(1)

    # assume that the vm code dir is a subdir of ../vm/
    vm_input = os.path.join("..", "vm", sys.argv[1])
    # and the output assembly will be in ../bin/
    out_filename = os.path.join("..", "asm", os.path.splitext(sys.argv[1])[0] + ".asm")
    
    if vm_input.endswith(".vm"): # input is file name
        vm_filenames = [vm_input]
    else: # input is dir name
        vm_filenames = [os.path.join("..", "vm", vm_input, f) for f in os.listdir(vm_input) if f.endswith(".vm")]
    
    vm_translator = VMTranslator(vm_filenames, out_filename)
    vm_translator.parse()


if __name__ == "__main__":
    main()