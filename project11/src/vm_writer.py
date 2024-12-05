from typing import TextIO, Literal

_Segment = Literal["constant", "argument", "local", "static", "this", "that", "pointer", "temp"]
_Command = Literal["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

class VMWriter:
    """
    Writes VM commands to an output file in the VM language.
    """
    def __init__(self, outfile: TextIO):
        self.outfile = outfile

    def write_push(self, segment: _Segment, index: int) -> None:
        self.outfile.write(f"push {segment} {index}\n")

    def write_pop(self, segment: _Segment, index: int) -> None:
        self.outfile.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: _Command) -> None:
        self.outfile.write(f"{command}\n")

    def write_label(self, label: str) -> None:
        self.outfile.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        self.outfile.write(f"goto {label}\n")

    def write_if_goto(self, label: str) -> None:
        self.outfile.write(f"if-goto {label}\n")

    def write_function(self, name: str, num_locals: int) -> None:
        self.outfile.write(f"function {name} {num_locals}\n")

    def write_call(self, name: str, num_args: int) -> None:
        self.outfile.write(f"call {name} {num_args}\n")

    def write_return(self) -> None:
        self.outfile.write("return\n")