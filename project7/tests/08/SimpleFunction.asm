
        (SimpleFunction.test)
        
        @2
        D=A

        (SETUPLOOP.SimpleFunction.test)
        @ENDSETUP.SimpleFunction.test
        D;JEQ
        
                @0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        D=D-1
        @SETUPLOOP.SimpleFunction.test
        
        (ENDSETUP.SimpleFunction.test)
        
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
        
                
                @LCL
                D=M // get the base address of the wanted segment
                @1
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
        
            
            
        @SP
        M=M-1
        A=M
        
            M=!M

            
        @SP
        M=M+1
        
            
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
        

            
        @SP
        M=M-1
        A=M
        
            M=D+M

            
        @SP
        M=M+1
        
            
                @ARG
                D=M // get the base address of the wanted segment
                @1
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
        
            
        // save lcl/frame address to R13
        @LCL
        D=A
        @R13
        M=D

        // save return address to R14
        @5
        A=D-A
        D=M
        @R14
        M=D

        // pop return data to arg 0
        
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
                

        // SP = ARG + 1
        @ARG
        D=M
        @SP
        M=D+1

        @R13
        D=M
        D=D-1
        @THAT
        M=D
        D=D-1
        @THIS
        M=D
        D=D-1
        @ARG
        M=D
        D=D-1
        @LCL
        M=D
        D=D-1

        @R14
        A=M
        0;JMP
        