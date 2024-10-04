import os, sys
from code_writer import CodeWriter

class VMTranslator:
    def __init__(self, vm_input: str):
        """
        Initializes the VMTranslator with the input VM file or directory.

        Args:
            vm_input (str): Path to the input VM file or directory containing VM files.
        """
        # use os.path.splitext to remove file extension if there's any
        self.out_filename = os.path.splitext(sys.argv[1])[0] + ".asm"

        # remove path and keep only the file | dir name by itself
        program_name = os.path.basename(vm_input)
        if vm_input.endswith(".vm"): # input is file name
            # use the user input vm program name as the code writer's name (to be used in static push pop)
            self.code_writer = CodeWriter(os.path.splitext(program_name)[0])
            vm_filenames = [vm_input]
        else: # input is dir name
            self.code_writer = CodeWriter(program_name)
            # grab all the .vm files in the dir
            vm_filenames = [os.path.join(vm_input, f) for f in os.listdir(vm_input) if f.endswith(".vm")]      
        self.vm_filenames = vm_filenames


    def get_command_type(self, command: str) -> str:
        """
        Determines the type of VM command.

        Args:
            command (str): The VM command string.

        Returns:
            str: The command type ("C_PUSH", "C_POP", "C_ARITHMETIC", etc.).
        """
        if command.startswith("push"):
            return "C_PUSH"
        if command.startswith("pop"):
            return "C_POP"
        if command.startswith(("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")):
            return "C_ARITHMETIC"
        if command.startswith("label"):
            return "C_LABEL"
        if command.startswith("goto"):
            return "C_GOTO"
        if command.startswith("if-goto"):
            return "C_IF"
        if command.startswith("function"):
            return "C_FUNCTION"
        if command.startswith("call"):
            return "C_CALL"
        if command.startswith("return"):
            return "C_RETURN"

        raise ValueError(f"Unknown command: {command}")
        

    def parse(self) -> None:
        """
        Parses VM files and translates them into Hack assembly code.

        Reads each VM file and generates the corresponding assembly code,
        which is written to the output file.
        """
        for vm_filename in self.vm_filenames:
            with open(vm_filename, "r") as infile, open(self.out_filename, "w") as outfile:
                for key, line in enumerate(infile): # use line num as the key for code writer arithmetic
                    if line.strip().startswith("//") or not line.strip():
                        continue # ignore empty line/ comment
                    
                    line = line.split("//")[0].strip()
                    command_type = self.get_command_type(line)
                    command_components = line.split()
                    
                    if command_type == "C_ARITHMETIC": # only 1 component
                        asm = self.code_writer.write_arithmetic(command_components[0], key)
                    elif command_type in ("C_PUSH", "C_POP"): 
                        # assume only ("C_PUSH", "C_POP") e.g. push local 0
                        # will have to refactor this in the future to support function and call commands
                        command, segment, idx = command_components
                        asm = self.code_writer.write_push_pop(command, segment, idx)
                    elif command_type == "C_LABEL":
                        asm = self.code_writer.write_label(command_components[1])
                    elif command_type == "C_GOTO":
                        asm = self.code_writer.write_goto(command_components[1])
                    elif command_type == "C_IF":
                        asm = self.code_writer.write_if(command_components[1])
                    elif command_type == "C_FUNCTION":
                        asm = self.code_writer.write_function(command_components[1], int(command_components[2]))
                    elif command_type == "C_CALL":
                        asm = self.code_writer.write_call(command_components[1], int(command_components[2]))
                    elif command_type == "C_RETURN":
                        asm = self.code_writer.write_return()

                    outfile.write(asm)

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <vm-directory | vm-file-path>")
        sys.exit(1)
    
    # assume user input is valid
    vm_translator = VMTranslator(sys.argv[1])
    vm_translator.parse()


if __name__ == "__main__":
    main()