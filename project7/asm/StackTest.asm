
@17
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@17
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

@SET_TRUE.9
D;JEQ // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.9
0;JMP

(SET_TRUE.9)
@SP
A=M
M=-1

(END.9)

@SP
M=M+1

            
@17
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@16
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

@SET_TRUE.12
D;JEQ // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.12
0;JMP

(SET_TRUE.12)
@SP
A=M
M=-1

(END.12)

@SP
M=M+1

            
@16
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@17
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

@SET_TRUE.15
D;JEQ // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.15
0;JMP

(SET_TRUE.15)
@SP
A=M
M=-1

(END.15)

@SP
M=M+1

            
@892
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@891
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

@SET_TRUE.18
D;JLT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.18
0;JMP

(SET_TRUE.18)
@SP
A=M
M=-1

(END.18)

@SP
M=M+1

            
@891
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@892
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

@SET_TRUE.21
D;JLT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.21
0;JMP

(SET_TRUE.21)
@SP
A=M
M=-1

(END.21)

@SP
M=M+1

            
@891
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@891
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

@SET_TRUE.24
D;JLT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.24
0;JMP

(SET_TRUE.24)
@SP
A=M
M=-1

(END.24)

@SP
M=M+1

            
@32767
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@32766
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

@SET_TRUE.27
D;JGT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.27
0;JMP

(SET_TRUE.27)
@SP
A=M
M=-1

(END.27)

@SP
M=M+1

            
@32766
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@32767
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

@SET_TRUE.30
D;JGT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.30
0;JMP

(SET_TRUE.30)
@SP
A=M
M=-1

(END.30)

@SP
M=M+1

            
@32766
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@32766
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

@SET_TRUE.33
D;JGT // the relation between the diff and 0 is the same as the relation between the two elements we want to compare
@SP
A=M
M=0
@END.33
0;JMP

(SET_TRUE.33)
@SP
A=M
M=-1

(END.33)

@SP
M=M+1

            
@57
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@31
D=A

@SP
A=M
M=D


@SP
M=M+1

        
@53
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

            
@112
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

            

@SP
M=M-1
A=M

M=-M


@SP
M=M+1

            

@SP
M=M-1
A=M
D=M



@SP
M=M-1
A=M

M=D&M


@SP
M=M+1

            
@82
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

M=D|M


@SP
M=M+1

            

@SP
M=M-1
A=M

M=!M


@SP
M=M+1

            