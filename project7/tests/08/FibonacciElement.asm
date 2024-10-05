
        @256
        D=A
        @SP
        M=D
        
        
        
                @FibonacciElement$RETURN.0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                

        @LCL
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @ARG
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THIS
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THAT
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        // D = n + 5
        @0
        D=A
        @5
        D=D+A

        // arg = sp-n-5 = sp-(n+5)
        @SP
        D=M-D
        @ARG
        M=D

        // lcl = sp
        @SP
        D=M
        @LCL
        M=D

        @FibonacciElement$Sys.init
        0;JMP
        
        (FibonacciElement$RETURN.0)
        
        
        (FibonacciElement$Main.fibonacci)
        
        @0
        D=A
        @R13
        M=D

        (FibonacciElement$SETUPLOOP.Main.fibonacci)
        @FibonacciElement$ENDSETUP.Main.fibonacci
        D;JEQ
        
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
        
                
        @R13
        MD=M-1
        @FibonacciElement$SETUPLOOP.Main.fibonacci
        0;JMP
        
        (FibonacciElement$ENDSETUP.Main.fibonacci)
        
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
        
                
                @2
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
        
            D=M-D
            // D now stores the difference between the previous two tops of the stack
            // now we need to run conditional check

            @FibonacciElement$SET_TRUE.14
            D;JLT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
            @SP
            A=M
            M=0
            @FibonacciElement$END.14
            0;JMP

            (FibonacciElement$SET_TRUE.14) // need the key to differentiate among potentially many @SET_TRUE generated by different commands in a Hack program
            @SP
            A=M
            M=-1

            (FibonacciElement$END.14)
            
        @SP
        M=M+1
        
            
        
        @SP
        M=M-1
        A=M
        D=M
        
        @FibonacciElement$N_LT_2
        D;JNE
        
        @FibonacciElement$N_GE_2
        0;JMP
        (FibonacciElement$N_LT_2)
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
        
                
        // save lcl/frame address to R15
        @LCL
        D=M
        @R15
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

        @R15
        AM=M-1
        D=M
        @THAT
        M=D

        @R15
        AM=M-1
        D=M
        @THIS
        M=D

        @R15
        AM=M-1
        D=M
        @ARG
        M=D
        
        @R15
        AM=M-1
        D=M
        @LCL
        M=D

        @R14
        A=M
        0;JMP
        (FibonacciElement$N_GE_2)
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
        
                
                @2
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
        
            
        
                @FibonacciElement$RETURN.24
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                

        @LCL
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @ARG
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THIS
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THAT
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        // D = n + 5
        @1
        D=A
        @5
        D=D+A

        // arg = sp-n-5 = sp-(n+5)
        @SP
        D=M-D
        @ARG
        M=D

        // lcl = sp
        @SP
        D=M
        @LCL
        M=D

        @FibonacciElement$Main.fibonacci
        0;JMP
        
        (FibonacciElement$RETURN.24)
        
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
        
            
        
                @FibonacciElement$RETURN.28
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                

        @LCL
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @ARG
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THIS
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THAT
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        // D = n + 5
        @1
        D=A
        @5
        D=D+A

        // arg = sp-n-5 = sp-(n+5)
        @SP
        D=M-D
        @ARG
        M=D

        // lcl = sp
        @SP
        D=M
        @LCL
        M=D

        @FibonacciElement$Main.fibonacci
        0;JMP
        
        (FibonacciElement$RETURN.28)
        
            
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
        
            
        // save lcl/frame address to R15
        @LCL
        D=M
        @R15
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

        @R15
        AM=M-1
        D=M
        @THAT
        M=D

        @R15
        AM=M-1
        D=M
        @THIS
        M=D

        @R15
        AM=M-1
        D=M
        @ARG
        M=D
        
        @R15
        AM=M-1
        D=M
        @LCL
        M=D

        @R14
        A=M
        0;JMP
        
        (FibonacciElement$Sys.init)
        
        @0
        D=A
        @R13
        M=D

        (FibonacciElement$SETUPLOOP.Sys.init)
        @FibonacciElement$ENDSETUP.Sys.init
        D;JEQ
        
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
        
                
        @R13
        MD=M-1
        @FibonacciElement$SETUPLOOP.Sys.init
        0;JMP
        
        (FibonacciElement$ENDSETUP.Sys.init)
        
                @4
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        
                @FibonacciElement$RETURN.15
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                

        @LCL
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @ARG
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THIS
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        @THAT
        D=M
        
        @SP
        A=M
        M=D
        
        
        @SP
        M=M+1
        

        // D = n + 5
        @1
        D=A
        @5
        D=D+A

        // arg = sp-n-5 = sp-(n+5)
        @SP
        D=M-D
        @ARG
        M=D

        // lcl = sp
        @SP
        D=M
        @LCL
        M=D

        @FibonacciElement$Main.fibonacci
        0;JMP
        
        (FibonacciElement$RETURN.15)
        (FibonacciElement$END)
        @FibonacciElement$END
        0;JMP
        