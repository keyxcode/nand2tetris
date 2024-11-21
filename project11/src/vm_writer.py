from typing import TextIO, Literal

_Segment = Literal["constant", "argument", "local", "static", "this", "that", "pointer", "temp"]
_Command = Literal["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

class VMWriter:
    def __init__(self, outfile: TextIO):
        self.outfile = outfile

    def write_push(self, segment: _Segment, index: int) -> None:
        self.outfile.write(f"push {segment} {index}")

    def write_pop(self, segment: _Segment, index: int) -> None:
        self.outfile.write(f"pop {segment} {index}")

    def write_arithmetic(self, command: _Command) -> None:
        self.outfile.write(command)

    def write_label(self, label: str) -> None:
        self.outfile.write(f"label {label}")

    def write_goto(self, label: str) -> None:
        self.outfile.write(f"goto {label}")

    def write_if_goto(self, label: str) -> None:
        self.outfile.write(f"if-goto {label}")

    def write_function(self, name: str, num_locals: int) -> None:
        self.outfile.write(f"function {name} {num_locals}")

    def write_call(self, name: str, num_args: int) -> None:
        self.outfile.write(f"call {name} {num_args}")

    def write_return(self) -> None:
        self.outfile.write("return")

    # def close(self) -> None:
    #     pass