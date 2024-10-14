
        @256
        D=A
        @SP
        M=D
        
        
        
                @$RETURN.0
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

        @Sys.init
        0;JMP
        
        ($RETURN.0)
        
        
        (Sys.init)
        
        @0
        D=A
        @R13
        M=D

        (Sys$SETUPLOOP.Sys.init)
        @Sys$ENDSETUP.Sys.init
        D;JEQ
        
                @0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        @R13
        MD=M-1
        @Sys$SETUPLOOP.Sys.init
        0;JMP
        
        (Sys$ENDSETUP.Sys.init)
        
                @4000
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
                
                @5000
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
                
        
                @Sys$RETURN.11
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

        @Sys.main
        0;JMP
        
        (Sys$RETURN.11)
        
                // get the exact address we want to go to
                @5
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
                (Sys$LOOP)
        @Sys$LOOP
        0;JMP
        
        (Sys.main)
        
        @5
        D=A
        @R13
        M=D

        (Sys$SETUPLOOP.Sys.main)
        @Sys$ENDSETUP.Sys.main
        D;JEQ
        
                @0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        @R13
        MD=M-1
        @Sys$SETUPLOOP.Sys.main
        0;JMP
        
        (Sys$ENDSETUP.Sys.main)
        
                @4001
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
                
                @5001
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
                
                @200
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @LCL
                D=M
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
                
                @40
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @LCL
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
                
                @6
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // get the exact address we want to go to
                @LCL
                D=M
                @3
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
                
                @123
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        
                @Sys$RETURN.34
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

        @Sys.add12
        0;JMP
        
        (Sys$RETURN.34)
        
                // get the exact address we want to go to
                @5
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
        
                
                @LCL
                D=M // get the base address of the wanted segment
                @2
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @LCL
                D=M // get the base address of the wanted segment
                @3
                A=D+A // get the exact address we want, and go there via A
                D=M // get the data stored there to D

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @LCL
                D=M // get the base address of the wanted segment
                @4
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
        
        (Sys.add12)
        
        @0
        D=A
        @R13
        M=D

        (Sys$SETUPLOOP.Sys.add12)
        @Sys$ENDSETUP.Sys.add12
        D;JEQ
        
                @0
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        @R13
        MD=M-1
        @Sys$SETUPLOOP.Sys.add12
        0;JMP
        
        (Sys$ENDSETUP.Sys.add12)
        
                @4002
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
                
                @5002
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
        
                
                @12
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
        