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
