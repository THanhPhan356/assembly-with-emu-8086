; Original midterm exercise 2, preserved for tracing and diagnosis.
; The supplied values overflow the 32-bit sum and the 16-bit DIV quotient.
; Expected behavior: division error at DIV CX, not a completed quotient.

.MODEL SMALL
.STACK 100h

.DATA
NUMBERS DW 10A0h, 20E0h
        DW 30B0h, 40F0h
        DW 50C0h, 6000h
        DW 70D0h, 8000h

DIVISOR       DW 03E8h
SUM_LOW       DW 0
SUM_HIGH      DW 0
QUOTIENT_LOW  DW 0
QUOTIENT_HIGH DW 0

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV SUM_LOW, 0
    MOV SUM_HIGH, 0
    LEA SI, NUMBERS
    MOV CX, 4

LOOP_SUM:
    MOV AX, [SI]
    ADD SUM_LOW, AX
    MOV AX, [SI+2]
    ADC SUM_HIGH, AX
    ADD SI, 4
    LOOP LOOP_SUM

    MOV DX, SUM_HIGH
    MOV AX, SUM_LOW
    MOV CX, DIVISOR
    DIV CX

    MOV QUOTIENT_LOW, AX
    MOV QUOTIENT_HIGH, 0

    MOV AH, 4Ch
    INT 21h
MAIN ENDP

END MAIN
