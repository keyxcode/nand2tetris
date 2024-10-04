class CodeWriter:
    def __init__(self, name: str):
        """
        Initializes the CodeWriter with segment mappings and code snippets.

        Args:
            name (str): The basename of the output program.
        """
        self.name = name # used for static segment symbols

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
            "that": "THAT",
            "pointer": 3,
            "temp": 5
        }

        #==========
        # some useful code snippets
        
        # decrement the stack pointer 
        # retrieve the value at the new top of the stack and assign it to the D register
        # affects all CPU registers
        self.POP_STACK_TO_D = '''
        @SP
        M=M-1
        A=M
        D=M
        '''

        # decrement the stack pointer
        # enable M to get the value at the top of the stack
        # does not affect D register
        self.GET_STACK_TO_M = '''
        @SP
        M=M-1
        A=M
        '''

        # put the data from D register to top of the stack
        # typically followed by INCREMENT_STACK_POINTER to complete a stack push operation
        # affects all CPU registers
        self.PUT_D_IN_STACK = '''
        @SP
        A=M
        M=D
        '''

        # increment the stack pointer
        # get ready for future push operations
        # does not affect D register
        self.INCREMENT_STACK_POINTER = '''
        @SP
        M=M+1
        '''

    def write_arithmetic(self, command: str, key: int) -> str:
        """
        Generates Hack assembly code for the specified VM command.

        Args:
            command (str): Arithmetic command ("add", "sub", "and", "or", "neg", "not", "eq", "gt", "lt").
            key (int): Unique key for labeling conditional jumps.
        Returns:
            str: Generated assembly code.
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

            (SET_TRUE.{key}) // need the key to differentiate among potentially many @SET_TRUE generated by different commands in a Hack program
            @SP
            A=M
            M=-1

            (END.{key})
            {self.INCREMENT_STACK_POINTER}
            '''

        return asm

    def write_push_pop(self, command: str, segment: str, idx: int) -> str:
        """
        Generates Hack assembly code for push or pop commands.

        Args:
            command (str): Command type ("push" or "pop").
            segment (str): Segment name ("constant", "local", "argument", "this", "that", "pointer", "temp", "static").
            idx (int): Index for the push/pop operation.

        Returns:
            str: Generated assembly code.
        """
        if command == "push":
            if segment == "constant":
                asm = f'''
                @{idx}
                D=A

                {self.PUT_D_IN_STACK}

                {self.INCREMENT_STACK_POINTER}
                '''
            elif segment in ("local", "argument", "this", "that"):
                # the corresponding memory pointer (RAM register) stores the base address of the segment we're trying to access
                mem_pointer = self.mem_pointer_lookup[segment]
                asm = f'''
                @{mem_pointer}
                D=M // get the base address of the wanted segment
                @{idx}
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                {self.PUT_D_IN_STACK}

                {self.INCREMENT_STACK_POINTER}
                '''
            elif segment in ("pointer", "temp"):
                # in this case, we go to the RAM register and use the data stored there itself
                # instead of using it as an address and making an additional jump
                base = 3 if segment == "pointer" else 5
                asm = f'''
                @{base}
                D=A // subtle difference compared to the case above
                @{idx}
                A=D+A
                D=M

                {self.PUT_D_IN_STACK}

                {self.INCREMENT_STACK_POINTER}
                '''
            else: # segment == "static"
                asm = f'''
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @{self.name}.{idx}
                D=M

                {self.PUT_D_IN_STACK}

                {self.INCREMENT_STACK_POINTER}
                '''

        elif command == "pop":
            # there's no constant case for pop because it wouldn't make sense
            # as constant is a pure virtual segment
            
            if segment in ("local", "argument", "this", "that"):
                mem_pointer = self.mem_pointer_lookup[segment]
                asm = f'''
                // get the exact address we want to go to
                @{mem_pointer}
                D=M
                @{idx}
                D=D+A
                
                // store that address to R13 (free register)
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                {self.POP_STACK_TO_D}

                // set the value at RAM register with address at R13 to D
                @R13
                A=M
                M=D
                '''
            elif segment in ("pointer", "temp"):
                base = 3 if segment == "pointer" else 5
                asm = f'''
                // get the exact address we want to go to
                @{base}
                D=A
                @{idx}
                D=D+A

                // store that address to R13 (free register)
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                {self.POP_STACK_TO_D}

                // set the value at RAM register with address at R13 to D
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
    

    def write_label(self, label: str) -> str:
        asm = f"({label})"

        return asm


    def write_goto(self, label: str) -> str:
        asm = f'''
        @{label}
        0;JMP
        '''

        return asm

    def write_if(self, label: str) -> str:
        asm = f'''
        {self.POP_STACK_TO_D}
        @{label}
        D;JNE
        '''

        return asm