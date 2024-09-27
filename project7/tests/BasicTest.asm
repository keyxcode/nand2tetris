
                @10
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @LCL
                D=M
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
                
                @21
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                @22
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @ARG
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
                
                // store the mem segment address to R13 (free register)
                @ARG
                D=M
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
                
                @36
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @THIS
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
                
                @42
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                @45
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @THAT
                D=M
                @5
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
                
                // store the mem segment address to R13 (free register)
                @THAT
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
                
                @510
                D=A

                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // store the mem segment address to R13 (free register)
                @5
                D=A
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
                
                // find the value of the element to push and save it to D
                @LCL
                D=M
                @0
                A=D+A
                D=M

                // push the value in D to the stack
                @SP
                A=M
                M=D

                
        @SP
        M=M+1
        
                
                // find the value of the element to push and save it to D
                @THAT
                D=M
                @5
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
                @ARG
                D=M
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
        
            M=M-D

            
        @SP
        M=M+1
        
            
                // find the value of the element to push and save it to D
                @THIS
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
        
                
                // find the value of the element to push and save it to D
                @THIS
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
        
            
                // find the value at the element to push and save it to D
                @5
                D=A
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
        
            