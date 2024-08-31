import sys
from typing import Dict, Optional


def init_symbol_table() -> Dict[str, str]:
    symbol_table = {
        "SP": format(0, f"015b"),
        "LCL": format(1, f"015b"),
        "ARG": format(2, f"015b"),
        "THIS": format(3, f"015b"),
        "THAT": format(4, f"015b"),
        **{("R" + str(i)): format(i, f"015b") for i in range(16)},
        "SCREEN": format(16384, f"015b"),
        "KBD": format(24576, f"015b"),
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


def parse(in_filename: str, out_filename: str, symbol_table: Dict[str, str]) -> None:
    # go through the entire program line by line
    # - preprocess (remove whitespace, ignore empty lines) - done
    # - determine if instruction is A/C/L (pseudo label instruction) - done
    # - translate A inst to 0address - done
    # - each time an A-instruction with symbol is encountered, see if it's already in the symbol table
    # - if yes, read from it, else enter (new symbol : free RAM slot (starting at address 16)) to the table
    # - translate C inst using the code module - done
    # - write each translated line to out - done

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

    base_memory = 16
    with open(in_filename, "r") as infile, open(out_filename, "w") as outfile:
        for line in infile:
            line = line.strip()
            if line == "" or line[0] in "/(":
                continue

            if line[0] == "@":  # A instruction
                address = line[1:]
                try:
                    out_line = "0" + format(int(address), f"015b")
                except ValueError:
                    if address in symbol_table:
                        out_line = "0" + symbol_table[address]
                    else:
                        symbol_table[address] = format(int(base_memory), f"015b")
                        out_line = "0" + symbol_table[address]
                        base_memory += 1

            else:  # C instruction
                parts = get_c_parts(line)
                comp = code.translate(parts[0], 0)
                dest = code.translate(parts[1], 1)
                jump = code.translate(parts[2], 2)
                out_line = "111" + comp + dest + jump

            outfile.write(out_line + "\n")


def read_label_symbols(filename: str, symbol_table: Dict[str, str]) -> None:
    # keep track of valid code line number
    # each time encounter a label line (starts with ( ), enter (program’s labels : next line count aka ROM address) to the symbol table
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
            symbol_table[label] = format(line_num + 1, f"015b")


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename>")
        sys.exit(1)

    in_filename = sys.argv[1]
    out_filename = in_filename.split(".")[0] + ".hack"

    symbol_table = init_symbol_table()
    read_label_symbols(in_filename, symbol_table)
    parse(in_filename, out_filename, symbol_table)


if __name__ == "__main__":
    main()
