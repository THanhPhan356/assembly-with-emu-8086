.MODEL SMALL
.STACK 100h

.DATA
; Low word first, high word second
a     dw 0FFFFh, 0FFFFh   ; FFFFFFFFh
b     dw 0001h, 0000h     ; 00000001h

sum   dw 0, 0
carry dw 0

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax         ; EXE startup DS points to the PSP, not our data.

; Add the low 16-bit words
mov ax, [a]
add ax, [b]

; Add the high 16-bit words and the carry
mov dx, [a + 2]
adc dx, [b + 2]

; Extract the 33rd bit: MOV preserves CF
mov cx, 0
adc cx, 0

; Store the result
mov [sum], ax
mov [sum + 2], dx
mov [carry], cx
    mov ah, 4Ch
    int 21h
MAIN ENDP

END MAIN
