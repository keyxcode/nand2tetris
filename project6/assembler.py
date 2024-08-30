import sys
from typing import Dict


def symbol_table() -> Dict[str, str]:
    table = dict()
    return table


def first_pass(filename: str) -> None:
    # go through the entire program line by line
    # enter (program’s labels : their ROM addresses) to the symbol table
    with open(filename, "r") as file:
        for line in file:
            pass


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

    filename = sys.argv[1]

    first_pass(filename)
    second_pass(filename)


if __name__ == "__main__":
    main()
