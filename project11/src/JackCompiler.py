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
        xml_filename = os.path.splitext(jack_filename)[0] + ".xml"
        vm_filename = os.path.splitext(jack_filename)[0] + ".vm"
        
        with open(jack_filename, "r") as infile, open(xml_filename, "a") as xml_out, open(vm_filename, "a") as vm_out:
            # clear the output files if already exist
            xml_out.truncate(0)
            xml_out.seek(0)
            vm_out.truncate(0)
            vm_out.seek(0)

            compilation_engine = CompilationEngine(infile, xml_out, vm_out)
            compilation_engine.compile_class()


if __name__ == "__main__":
    main()