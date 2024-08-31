import os, sys
from typing import Dict, List, TextIO
from utils import to_binary
from symbol_table import init_symbol_table, read_label_symbols
from translator import CTranslator


class Assembler:
    """
    Handles the assembly of a Hack assembly program into Hack binary machine code.

    Attributes:
        symbol_table (Dict[str, str]): Maps symbols to binary addresses.
        code (Code): Translates C-instruction fields to binary.
        base_memory (int): Starting address for new A-instruction symbols in RAM, starting at 16.

    Methods:
        parse(in_filename: str, out_filename: str) -> None
        _handle_a_instruction(line: str, outfile: TextIO) -> None
        _handle_c_instruction(line: str, outfile: TextIO) -> None
        _get_c_parts(instruction: str) -> Dict[Optional[str], str]
    """

    def __init__(self, symbol_table: Dict[str, str]):
        self.symbol_table = symbol_table
        self.c_translator = CTranslator()
        self.base_memory = 16

    def parse(self, in_filename: str, out_filename: str) -> None:
        """
        Translates an assembly source file into binary code and writes the result to an output file.

        Args:
            in_filename (str): Path to the input assembly file.
            out_filename (str): Path to the output file for binary code.
        """
        with open(in_filename, "r") as infile, open(out_filename, "w") as outfile:
            for line in infile:
                # preprocess
                line = line.strip()  # remove whitespace
                if line == "" or line[0] in "/(":
                    continue  # ignore empty/ comment/ label line

                if line[0] == "@":  # A-instruction
                    self._handle_a_instruction(line, outfile)
                else:  # C-instruction
                    self._handle_c_instruction(line, outfile)

    def _handle_a_instruction(self, line: str, outfile: TextIO) -> None:
        """
        Processes an A-instruction and writes its binary representation to the output file.

        Each time a symbolic A-instruction is encountered, check if the symbol is already in the symbol table
        If it is, read from it, else enter (new symbol : free RAM slot (starting at address 16)) to the table`
        The binary representation is written to the output file.

        Args:
            line (str): The A-instruction line from the input file.
            outfile (TextIO): The file object to write the binary output to.
        """
        address = line[1:]

        try:  # valid integer address
            out_line = "0" + to_binary(int(address))
        except ValueError:  # symbolic address (variable (RAM) or label (ROM))
            if address in self.symbol_table:
                out_line = "0" + self.symbol_table[address]
            else:
                self.symbol_table[address] = to_binary(int(self.base_memory))
                out_line = "0" + self.symbol_table[address]
                self.base_memory += 1

        outfile.write(out_line + "\n")

    def _handle_c_instruction(self, line: str, outfile: TextIO) -> None:
        """
        Processes a C-instruction and writes its binary representation to the output file.

        The method extracts the `comp`, `dest`, and `jump` fields and translates them using the `Code` class.
        The binary representation is written to the output file.

        Args:
            line (str): The C-instruction line from the input file.
            outfile (TextIO): The file object to write the binary output to.
        """
        # fields is in the format of [comp, dest, jump]
        fields = self._get_c_fields(line)
        translated_fields = [
            self.c_translator.translate(inst, i) for i, inst in enumerate(fields)
        ]
        out_line = "111" + "".join(translated_fields)

        outfile.write(out_line + "\n")

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
        print("Usage: python assembler.py <filename>")
        sys.exit(1)

    # assume that the assembly code file is found in ../asm/
    # and the output binary will be in ../bin/
    in_filename = os.path.join("asm", sys.argv[1])
    out_filename = os.path.join("bin", os.path.splitext(sys.argv[1])[0] + ".hack")

    # first pass: read all the label symbols and their corresponding ROM address into the symbol table
    symbol_table = init_symbol_table()
    read_label_symbols(in_filename, symbol_table)

    # second pass: parse the assembly code
    assembler = Assembler(symbol_table)
    assembler.parse(in_filename, out_filename)


if __name__ == "__main__":
    main()
