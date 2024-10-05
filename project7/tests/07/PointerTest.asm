
                @3030
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @3
                D=A
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
                
                @3040
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @3
                D=A
                @1
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
                
                @32
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @THIS
                D=M
                @2
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
                
                @46
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @THAT
                D=M
                @6
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
                
                @3
                D=A // subtle difference compared to the case above
                @0
                A=D+A
                D=M

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @3
                D=A // subtle difference compared to the case above
                @1
                A=D+A
                D=M

                
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
        
            
                @THIS
                D=M // get the base address of the wanted segment
                @2
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
        
            M=M-D

            
        @SP
        M=M+1
        
            
                @THAT
                D=M // get the base address of the wanted segment
                @6
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
        
            