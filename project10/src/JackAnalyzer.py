import os, sys
from jack_tokenizer import JackTokenizer

class JackAnalyzer:
    def __init__(self, vm_input: str):
        pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <jack-directory | jack-file-path>")
        sys.exit(1)
    
    tokenizer = JackTokenizer(sys.argv[1])
    tokenizer.get_token()


if __name__ == "__main__":
    main()