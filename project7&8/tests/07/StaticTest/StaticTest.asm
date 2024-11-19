
                @111
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @333
                D=A

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                @888
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
        
                @StaticTest.8
                M=D
                
                
        @SP
        M=M-1
        A=M
        D=M
        
                @StaticTest.3
                M=D
                
                
        @SP
        M=M-1
        A=M
        D=M
        
                @StaticTest.1
                M=D
                
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @StaticTest.3
                D=M

                
        @SP
        A=M
        M=D
        

                
        @SP
        M=M+1
        
                
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @StaticTest.1
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
        
            
                // the first time this symbol is encountered (whether in push or pop)
                // it will be mapped to the next free RAM register starting from R16
                @StaticTest.8
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
        
            