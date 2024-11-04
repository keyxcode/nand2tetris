import os

class JackTokenizer:
    def __init__(self, jack_input: str):
        """
        Initializes the JackTokenizer with the input Jack file or directory.

        Args:
            jack_input (str): Path to the input Jack file or directory containing Jack files.
        """
        if jack_input.endswith(".jack"): # input is file name
            self.jack_filenames = [jack_input]
        else: # input is dir name
            self.jack_filenames = [os.path.join(jack_input, f) for f in os.listdir(jack_input) if f.endswith(".jack")]

    def parse(self) -> None:
        for jack_filename in self.jack_filenames:
            out_filename = os.path.splitext(jack_filename)[0] + "TM.xml"
            
            with open(jack_filename, "r") as infile, open(out_filename, "w") as outfile:
                for line in infile:
                    outfile.write(line)

    def has_more_tokens() -> bool:
        pass

    def advance() -> None:
        pass

    def token_type() -> None:
        pass

    def keyword() -> None:
        pass

    def symbol() -> str:
        pass

    def identifier() -> str:
        pass

    def int_val() -> int:
        pass

    def string_val() -> str:
        pass