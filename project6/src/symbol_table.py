from typing import Dict
from utils import to_binary


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
