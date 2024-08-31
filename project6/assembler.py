import sys
from typing import Dict, List, TextIO


def to_binary(value: int, bits: int = 15) -> str:
    """
    Convert an base-10 integer to a binary string with a specified number of bits.

    Args:
        value (int): The integer to convert.
        bits (int, optional): The number of bits for the binary representation. Defaults to 15 to suit Hack machine language address width.

    Returns:
        str: The binary string representation of the integer, zero-padded to the specified number of bits.
    """
    return format(value, f"0{bits}b")


def init_symbol_table() -> Dict[str, str]:
    """
    Create a symbol table with Hack predefined symbols and their 15-bit binary values.

    Returns:
        Dict[str, str]: Dictionary of symbol names and their binary string representations.
    """
    return {
        "SP": to_binary(0),
        "LCL": to_binary(1),
        "ARG": to_binary(2),
        "THIS": to_binary(3),
        "THAT": to_binary(4),
        **{("R" + str(i)): to_binary(i) for i in range(16)},
        "SCREEN": to_binary(16384),
        "KBD": to_binary(24576),
    }


def read_label_symbols(filename: str, symbol_table: Dict[str, str]) -> None:
    """
    Parses label symbols from an assembly file and updates the symbol table.

    Identifies label lines (lines that start with '(' and end with ')'), and maps each label to its corresponding ROM address.
    The ROM address is the number of the line of code right after the label.

    Args:
        filename (str): Path to the assembly file.
        symbol_table (Dict[str, str]): Dictionary to update with labels and their binary addresses.

    Returns:
        None: Updates `symbol_table` in place.
    """
    # starts with -1 so that the first line of code is registered as 0
    line_num = -1

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("//"):
                continue

            # valid assembly code
            if not line.startswith("("):
                line_num += 1
                continue

            # a label
            label = line.strip("()")
            symbol_table[label] = to_binary(line_num + 1)


class Code:
    """
    A class to handle the translation of Hack assembly C-instruction fields to binary code.

    Attributes:
        comp_dict (dict): A dictionary mapping computation mnemonics to their binary codes.
        dest_dict (dict): A dictionary mapping destination mnemonics to their binary codes.
        jump_dict (dict): A dictionary mapping jump mnemonics to their binary codes.

    Methods:
        translate(inst: str, field: int) -> str

    Raises:
        KeyError: If the provided instruction or field is invalid.
    """

    def __init__(self):
        self.comp_dict = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101",
        }
        self.dest_dict = {
            None: "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }
        self.jump_dict = {
            None: "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }

    def translate(self, inst: str, field: int) -> str:
        """
        Translates a Hack assembly C-instruction field to its binary representation.

        Args:
            inst (str): The C-instruction field (e.g., "D", "M", "JEQ").
            field (int): The type of field to translate:
                - 0: comp
                - 1: dest
                - 2: jump

        Returns:
            str: The binary representation of the instruction component.

        Raises:
            KeyError: If the instruction component or field is invalid.
        """

        if field == 0:
            return self.comp_dict[inst]
        elif field == 1:
            return self.dest_dict[inst]
        elif field == 2:
            return self.jump_dict[inst]
        else:
            raise KeyError("Invalid instruction {inst}")


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
        self.code = Code()
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

        comp = self.code.translate(fields[0], 0)
        dest = self.code.translate(fields[1], 1)
        jump = self.code.translate(fields[2], 2)

        out_line = "111" + comp + dest + jump
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

    in_filename = sys.argv[1]
    out_filename = in_filename.split(".")[0] + ".hack"

    symbol_table = init_symbol_table()
    read_label_symbols(in_filename, symbol_table)

    assembler = Assembler(symbol_table)
    assembler.parse(in_filename, out_filename)


if __name__ == "__main__":
    main()
