// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

// init some constants
// n=8912 (total num of screen ram registers)
@8192
D=A
@n
M=D
// address=SCREEN address in ram (16384)
@SCREEN
D=A
@address
M=D

(RESTART)
// reset i=0
@i
M=0
@LOOP
0;JMP

// draw loop
(LOOP)
// if i == n, restart
@i
D=M
@n
D=D-M
@RESTART
D;JEQ

@KBD
D=M
@WHITE
D;JEQ
@BLACK
D;JNE

(WHITE)
// set ram[address + i] = 0
@address
D=M
@i
A=D+M
M=0
@INCREMENT
0;JMP

(BLACK)
// set ram[address + i] = -1
@address
D=M
@i
A=D+M
M=-1
@INCREMENT
0;JMP

(INCREMENT)
// increment i
@i
M=M+1
@LOOP
0;JMP