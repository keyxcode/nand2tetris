
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
        
        
        (Class1.set)
        
        @0
        D=A
        @R13
        M=D

        (Class1$SETUPLOOP.Class1.set)
        @Class1$ENDSETUP.Class1.set
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
        @Class1$SETUPLOOP.Class1.set
        0;JMP
        
        (Class1$ENDSETUP.Class1.set)
        
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
        
                @Class1.0
                M=D
                
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
        
                @Class1.1
                M=D
                
                @0
                D=A

                
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
        
        (Class1.get)
        
        @0
        D=A
        @R13
        M=D

        (Class1$SETUPLOOP.Class1.get)
        @Class1$ENDSETUP.Class1.get
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
        @Class1$SETUPLOOP.Class1.get
        0;JMP
        
        (Class1$ENDSETUP.Class1.get)
        
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @Class1.0
                D=M

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @Class1.1
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
        
            M=M-D

            
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
        
                @6
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @8
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        
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
        @2
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

        @Class1.set
        0;JMP
        
        (Sys$RETURN.11)
        
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
                
                @23
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @15
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
        
                @Sys$RETURN.15
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
        @2
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

        @Class2.set
        0;JMP
        
        (Sys$RETURN.15)
        
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
                
        
                @Sys$RETURN.17
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

        @Class1.get
        0;JMP
        
        (Sys$RETURN.17)
        
        
                @Sys$RETURN.18
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

        @Class2.get
        0;JMP
        
        (Sys$RETURN.18)
        (Sys$END)
        @Sys$END
        0;JMP
        
        (Class2.set)
        
        @0
        D=A
        @R13
        M=D

        (Class2$SETUPLOOP.Class2.set)
        @Class2$ENDSETUP.Class2.set
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
        @Class2$SETUPLOOP.Class2.set
        0;JMP
        
        (Class2$ENDSETUP.Class2.set)
        
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
        
                @Class2.0
                M=D
                
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
        
                @Class2.1
                M=D
                
                @0
                D=A

                
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
        
        (Class2.get)
        
        @0
        D=A
        @R13
        M=D

        (Class2$SETUPLOOP.Class2.get)
        @Class2$ENDSETUP.Class2.get
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
        @Class2$SETUPLOOP.Class2.get
        0;JMP
        
        (Class2$ENDSETUP.Class2.get)
        
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @Class2.0
                D=M

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @Class2.1
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
        
            M=M-D

            
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
        