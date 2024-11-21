from typing import TextIO, Literal

_Segment = Literal["const", "arg", "local", "static", "this", "that", "pointer", "temp"]
_Command = Literal["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

class VMWriter:
    def __init__(self, outfile: TextIO):
        self.outfile = outfile

    def write_push(self, segment: _Segment, index: int) -> None:
        pass

    def write_pop(self, segment: _Segment, index: int) -> None:
        pass

    def write_arithmetic(self, command: _Command) -> None:
        pass

    def write_label(self, label: str) -> None:
        pass

    def write_goto(self, label: str) -> None:
        pass

    def write_if(self, label: str) -> None:
        pass

    def write_call(self, name: str, num_args: int) -> None:
        pass

    def write_function(self, name: str, num_locals: int) -> None:
        pass

    def write_return(self) -> None:
        pass

    # def close(self) -> None:
    #     pass