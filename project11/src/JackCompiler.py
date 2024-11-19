import os, sys
from compilation_engine import CompilationEngine

def main():
    if len(sys.argv) != 2:
        print("Usage: python JackCompiler.py <jack-directory | jack-file-path>")
        sys.exit(1)
    
    jack_input = sys.argv[1]
    if jack_input.endswith(".jack"): # input is file name
        jack_filenames = [jack_input]
    else: # input is dir name
        jack_filenames = [os.path.join(jack_input, f) for f in os.listdir(jack_input) if f.endswith(".jack")]

    for jack_filename in jack_filenames:
        # add M here to distinguish with the given parsed test file
        # need to remove later
        out_filename = os.path.splitext(jack_filename)[0] + ".xml"
        
        with open(jack_filename, "r") as infile, open(out_filename, "a") as outfile:
            compilation_engine = CompilationEngine(infile, outfile)
            compilation_engine.compile_class()


if __name__ == "__main__":
    main()