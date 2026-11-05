.MODEL SMALL
.STACK 100h

.DATA
N equ 5
A db -5, 0, 7, -12, 3
B db N dup(0)

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax         ; EXE startup DS points to the PSP, not our data.

start:
    mov si, 0           ; i = 0; each element occupies one byte

while_loop:
    cmp si, N
    jae end_while       ; Exit when i >= N (unsigned index comparison)

    mov al, A[si]       ; AL = A[i]
    cmp al, 0
    jge result          ; Nonnegative: skip negation
    neg al              ; Negative: AL = 0 - AL

result:
    mov B[si], al       ; B[i] = abs(A[i])
    inc si              ; i++
    jmp while_loop      ; Check the condition again

end_while:
    mov ah, 4Ch
    int 21h
MAIN ENDP

END MAIN
