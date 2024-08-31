class CTranslator:
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
