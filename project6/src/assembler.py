import os, sys
from typing import Dict, List
from utils import to_binary
from symbol_table import init_symbol_table, read_label_symbols
from translator import CTranslator


class Assembler:
    def __init__(self, asm_filepath: str, symbol_table: Dict[str, str]):
        """
        Initializes the Assembler to translate a Hack assembly program into Hack binary machine code.
        
        Args:
            asm_filepath (str): Path to the input assembly file.
            symbol_table (Dict[str, str]): Dict that maps symbols to binary addresses.
        """
        self.in_filepath = asm_filepath
        self.out_filepath = os.path.splitext(asm_filepath)[0] + ".hack"
        self.symbol_table = symbol_table
        self.c_translator = CTranslator()
        self.base_memory = 16 # RAM address counter for new A-instruction symbols, starting at 16.

    def parse(self) -> None:
        """
        Translates an assembly source file into binary code and writes the result to an output file.
        """
        with open(self.in_filepath, "r") as infile, open(self.out_filepath, "w") as outfile:
            for line in infile:
                # preprocess
                line = line.strip()  # remove whitespace
                if line == "" or line[0] in "/(":
                    continue  # ignore empty/ comment/ label line

                if line[0] == "@":  # A-instruction
                    bin_code = self._translate_a_instruction(line)
                else:  # C-instruction
                    bin_code = self._translate_c_instruction(line)
                
                outfile.write(bin_code + "\n")

    def _translate_a_instruction(self, line: str) -> str:
        """
        Processes an A-instruction and returns its binary representation.

        Each time a symbolic A-instruction is encountered, the method checks if the symbol 
        is already in the symbol table. If it is, it reads from it; otherwise, it enters
        the new symbol with a free RAM slot (starting at address 16) into the table.

        Args:
            line (str): The A-instruction line from the input file.

        Returns:
            str: The binary representation of the A-instruction.
        """
        address = line[1:]

        try:  # valid integer address
            bin_code = "0" + to_binary(int(address))
        except ValueError:  # symbolic address (variable (RAM) or label (ROM))
            if address in self.symbol_table:
                bin_code = "0" + self.symbol_table[address]
            else:
                self.symbol_table[address] = to_binary(int(self.base_memory))
                bin_code = "0" + self.symbol_table[address]
                self.base_memory += 1

        return bin_code

    def _translate_c_instruction(self, line: str) -> str:
        """
        Processes a C-instruction and returns its binary representation.

        The method extracts the `comp`, `dest`, and `jump` fields and translates them using the `Code` class.

        Args:
            line (str): The C-instruction line from the input file.

        Returns:
            str: The binary representation of the C-instruction.
        """
        # fields is in the format of [comp, dest, jump]
        fields = self._get_c_fields(line)
        translated_fields = [
            self.c_translator.translate(inst, i) for i, inst in enumerate(fields)
        ]
        bin_code = "111" + "".join(translated_fields)

        return bin_code

    def _get_c_fields(self, instruction: str) -> List[str]:
        """
        Parses a C-instruction into its component fields: comp, dest, and jump.

        Args:
            instruction (str): The C-instruction in the format of 'dest=comp;jump'.

        Returns:
            List[str]: A list of ['comp', 'dest', 'jump'] fields of the C-instruction.
        """
        fields = [None] * 3

        # split [left field, (maybe) jump]
        split1 = instruction.split(";")
        if len(split1) == 2:
            fields[2] = split1[1]

        # split [(maybe) dest, comp]
        split2 = split1[0].split("=")
        if len(split2) == 2:
            fields[1] = split2[0]

        fields[0] = split2[-1]

        return fields


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <asm-file-path>")
        sys.exit(1)

    # assume user input is valid
    asm_filepath = sys.argv[1]

    # first pass: read all the label symbols and their corresponding ROM address into the symbol table
    symbol_table = init_symbol_table()
    read_label_symbols(asm_filepath, symbol_table)

    # second pass: parse the assembly code
    assembler = Assembler(asm_filepath, symbol_table)
    assembler.parse()


if __name__ == "__main__":
    main()
