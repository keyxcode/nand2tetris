
                @3030
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @3
                D=A
                @0
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the mem segment to the value at R13
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
        
                
                // store the mem segment address to R13 (free register)
                @3
                D=A
                @1
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the mem segment to the value at R13
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
        
                
                // store the mem segment address to R13 (free register)
                @THIS
                D=M
                @2
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the mem segment to the value at R13
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
        
                
                // store the mem segment address to R13 (free register)
                @THAT
                D=M
                @6
                D=D+A
                @R13
                M=D

                // decrement the stack pointer and get the value there to D
                
        @SP
        M=M-1
        A=M
        D=M
        

                // set the mem segment to the value at R13
                @R13
                A=M
                M=D
                
                // find the value at the element to push and save it to D
                @3
                D=A
                @0
                A=D+A
                D=M

                // push the value in D to the stack
                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // find the value at the element to push and save it to D
                @3
                D=A
                @1
                A=D+A
                D=M

                // push the value in D to the stack
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
        
            
                // find the value of the element to push and save it to D
                @THIS
                D=M
                @2
                A=D+A
                D=M

                // push the value in D to the stack
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
        
            
                // find the value of the element to push and save it to D
                @THAT
                D=M
                @6
                A=D+A
                D=M

                // push the value in D to the stack
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
        
            