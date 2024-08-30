import sys
from typing import Dict


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


def parse(in_filename: str, out_filename: str) -> None:
    # go through the entire program line by line
    # - preprocess (remove whitespace, ignore empty lines)
    # - determine if instruction is A/C/L (pseudo label instruction)
    # - translate A inst to 0address
    # - translate C inst using the code module
    # - write each translated line to out

    # enter (program’s labels : their ROM addresses) to the symbol table???

    with open(in_filename, "r") as infile, open(out_filename, "w") as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line == "":
                continue

            if stripped_line[0] == "@":  # A instruction
                out_line = "0" + str(bin(int(stripped_line[1:])))
            elif stripped_line[0] == "(":  # L pseudo instruction
                pass  # ignore for now
            else:  # C instruction

                comp = ""
                dest = ""
                jump = ""
                out_line = "111" + comp + dest + jump

            outfile.write(out_line + "\n")


def second_pass(filename: str) -> None:
    # go through the entire program line by line and parse each instruction to binary
    # each time an A-instruction with symbol is encountered, see if it's already in the symbol table
    # if yes, read from it, else enter (new symbol : free RAM slot (starting at address 16)) to the table
    with open(filename, "r") as file:
        for line in file:
            pass


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
