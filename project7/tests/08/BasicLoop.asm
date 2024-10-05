

        
                @0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @LCL
                D=M
                @0
                D=D+A
                
                // store that address to R13 (free register)
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the value at RAM register with address at R13 to D
                @R13
                A=M
                M=D
                (BasicLoop$LOOP)
                @ARG
                D=M // get the base address of the wanted segment
                @0
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @LCL
                D=M // get the base address of the wanted segment
                @0
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
            
        @SP
        M=M-1
        A=M
        D=M
        

            
        @SP
        M=M-1
        A=M
        
            M=D+M

            
        @SP
        M=M+1
        
            
                // get the exact address we want to go to
                @LCL
                D=M
                @0
                D=D+A
                
                // store that address to R13 (free register)
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the value at RAM register with address at R13 to D
                @R13
                A=M
                M=D
                
                @ARG
                D=M // get the base address of the wanted segment
                @0
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @1
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
            
        @SP
        M=M-1
        A=M
        D=M
        

            
        @SP
        M=M-1
        A=M
        
            M=M-D

            
        @SP
        M=M+1
        
            
                // get the exact address we want to go to
                @ARG
                D=M
                @0
                D=D+A
                
                // store that address to R13 (free register)
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the value at RAM register with address at R13 to D
                @R13
                A=M
                M=D
                
                @ARG
                D=M // get the base address of the wanted segment
                @0
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        
        @SP
        M=M-1
        A=M
        D=M
        
        @BasicLoop$LOOP
        D;JNE
        
                @LCL
                D=M // get the base address of the wanted segment
                @0
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                