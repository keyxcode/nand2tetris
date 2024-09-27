class CodeWriter:
    def __init__(self, name: str):
        self.name = name

        self.operator_lookup = {
            "add": "+",
            "sub": "-",
            "and": "&",
            "or": "|",
            "neg": "-",
            "not": "!",
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT"
        }

        self.mem_pointer_lookup = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }

        #==========
        # some useful code snippets
        
        # decrement the stack pointer 
        # retrieve the value at the new top of the stack and assign it to the D register
        self.POP_STACK_TO_D = '''
        @SP
        M=M-1
        A=M
        D=M
        '''

        # decrement the stack pointer
        # enable future M read to get the value at the new top of the stack
        self.GET_STACK_TO_M = '''
        @SP
        M=M-1
        A=M
        '''

        # increment the stack pointer
        # get ready for future push operations
        self.INCREMENT_STACK_POINTER = '''
        @SP
        M=M+1
        '''

    def write_arithmetic(self, command: str, key: int) -> str:
        """
        Generates Hack assembly code for the specified arithmetic command.

        Args:
            command (str): Arithmetic command ("add", "sub", "and", "or", "neg", "not", "eq", "gt", "lt").
            key (int): Unique key for labeling conditional jumps.
        """

        op = self.operator_lookup[command]

        if command in ("add", "and", "or"):
            asm = f'''
            {self.POP_STACK_TO_D}

            {self.GET_STACK_TO_M}
            M=D{op}M

            {self.INCREMENT_STACK_POINTER}
            '''

        elif command == "sub":
            asm = f'''
            {self.POP_STACK_TO_D}

            {self.GET_STACK_TO_M}
            M=M{op}D

            {self.INCREMENT_STACK_POINTER}
            '''
        
        elif command in ("neg", "not"):
            asm = f'''
            {self.GET_STACK_TO_M}
            M={op}M

            {self.INCREMENT_STACK_POINTER}
            '''
            
        else: # command in ("eq", "gt", "lt"):
            asm = f'''
            {self.POP_STACK_TO_D}

            {self.GET_STACK_TO_M}
            D=M-D
            // D now stores the difference between the previous two tops of the stack
            // now we need to run conditional check

            @SET_TRUE.{key}
            D;{op} // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
            @SP
            A=M
            M=0
            @END.{key}
            0;JMP

            (SET_TRUE.{key})
            @SP
            A=M
            M=-1

            (END.{key})
            {self.INCREMENT_STACK_POINTER}
            '''

        return asm

    def write_push_pop(self, command: str, segment: str, idx: int) -> str:
        if command == "push":
            if segment == "constant":
                asm = f'''
                @{idx}
                D=A

                @SP
                A=M
                M=D

                {self.INCREMENT_STACK_POINTER}
                '''
            elif segment in ("local", "argument", "this", "that"):
                mem_pointer = self.mem_pointer_lookup[segment]
                asm = f'''
                // find the value of the element to push and save it to D
                @{mem_pointer}
                D=M
                @{idx}
                A=D+A
                D=M

                // push the value in D to the stack
                @SP
                A=M
                M=D

                {self.INCREMENT_STACK_POINTER}
                '''
            elif segment in ("pointer", "temp"):
                base = 3 if segment == "pointer" else 5
                asm = f'''
                // find the value at the element to push and save it to D
                @{base}
                D=A
                @{idx}
                A=D+A
                D=M

                // push the value in D to the stack
                @SP
                A=M
                M=D

                {self.INCREMENT_STACK_POINTER}
                '''
            else: # segment == "static"
                asm = f'''
                @{self.name}.{idx}
                D=M

                // push the value in D to the stack
                @SP
                A=M
                M=D

                {self.INCREMENT_STACK_POINTER}
                '''

        elif command == "pop":
            # there's no constant case for pop because it wouldn't make sense
            # as constant is a pure virtual segment
            
            if segment in ("local", "argument", "this", "that"):
                mem_pointer = self.mem_pointer_lookup[segment]
                asm = f'''
                // store the mem segment address to R13 (free register)
                @{mem_pointer}
                D=M
                @{idx}
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                {self.POP_STACK_TO_D}

                // set the mem segment to the value at R13
                @R13
                A=M
                M=D
                '''
            elif segment in ("pointer", "temp"):
                base = 3 if segment == "pointer" else 5
                asm = f'''
                // store the mem segment address to R13 (free register)
                @{base}
                D=A
                @{idx}
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                {self.POP_STACK_TO_D}

                // set the mem segment to the value at R13
                @R13
                A=M
                M=D
                '''
            else: # segment == "static"
                asm = f'''
                {self.POP_STACK_TO_D}
                @{self.name}.{idx}
                M=D
                '''

        return asm