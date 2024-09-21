import os, sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <vm-dir-name>")
        sys.exit(1)

    # assume that the vm code dir is a subdir of ../vm/
    # and the output assembly will be in ../bin/
    vm_dirname = os.path.join("vm", sys.argv[1])
    out_filename = os.path.join("bin", os.path.splitext(sys.argv[1])[0] + ".asm")
    print(vm_dirname, out_filename)

if __name__ == "__main__":
    main()