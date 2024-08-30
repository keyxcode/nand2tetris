import sys
from typing import Dict, Optional


def init_symbol_table() -> Dict[str, int]:
    symbol_table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        **{("R" + str(i)): i for i in range(16)},
        "SCREEN": 16384,
        "KBD": 24576,
    }
    return symbol_table


class Code:
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
        if field == 0:  # comp
            return self.comp_dict[inst]
        elif field == 1:  # dest
            return self.dest_dict[inst]
        elif field == 2:  # jump
            return self.jump_dict[inst]
        else:
            raise KeyError("Invalid instruction {inst}")


def parse(in_filename: str, out_filename: str) -> None:
    # go through the entire program line by line
    # - preprocess (remove whitespace, ignore empty lines)
    # - determine if instruction is A/C/L (pseudo label instruction)
    # - translate A inst to 0address
    # - translate C inst using the code module
    # - write each translated line to out

    # enter (program’s labels : their ROM addresses) to the symbol table???

    def get_c_parts(instruction: str) -> Dict[Optional[str], str]:
        # at index: 0 is comp, 1 is dest, 2 is jump
        parts = [None] * 3

        # split left part : (maybe) jump
        split1 = instruction.split(";")
        if len(split1) == 2:
            parts[2] = split1[1]

        # split (maybe) dest : comp
        split2 = split1[0].split("=")
        if len(split2) == 2:
            parts[1] = split2[0]

        parts[0] = split2[-1]
        return parts

    code = Code()

    with open(in_filename, "r") as infile, open(out_filename, "w") as outfile:
        for line in infile:
            line = line.strip()
            if line == "" or line.startswith("//"):
                continue

            if line[0] == "@":  # A instruction
                out_line = "0" + format(int(line[1:]), f"015b")
            else:  # C instruction
                parts = get_c_parts(line)
                comp = code.translate(parts[0], 0)
                dest = code.translate(parts[1], 1)
                jump = code.translate(parts[2], 2)
                out_line = "111" + comp + dest + jump
            # elif stripped_line[0] == "(":  # L pseudo instruction
            #     pass  # ignore for now

            outfile.write(out_line + "\n")


# def second_pass(filename: str) -> None:
#     # go through the entire program line by line and parse each instruction to binary
#     # each time an A-instruction with symbol is encountered, see if it's already in the symbol table
#     # if yes, read from it, else enter (new symbol : free RAM slot (starting at address 16)) to the table
#     with open(filename, "r") as file:
#         for line in file:
#             pass


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename>")
        sys.exit(1)

    in_filename = sys.argv[1]
    out_filename = in_filename.split(".")[0] + ".hack"

    # symbol_table = init_symbol_table()

    parse(in_filename, out_filename)

    # first_pass(filename)
    # second_pass(filename)


if __name__ == "__main__":
    main()
