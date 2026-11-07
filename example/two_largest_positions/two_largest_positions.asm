org 100h
jmp start

A    dw -7, 12, 5, 12, -2
N    dw 5
max1 dw 0
max2 dw 0
pos1 dw -1
pos2 dw -1

start:
    push cs
    pop ds

    mov pos1, -1
    mov pos2, -1
    cmp N, 2
    jb done

    mov ax, A[0]
    mov max1, ax
    mov pos1, 0
    mov si, 1

find_first:
    cmp si, N
    jae prepare_second

    mov bx, si
    shl bx, 1          ; Convert the element index to a byte offset
    mov ax, A[bx]
    cmp ax, max1
    jle next_first

    mov max1, ax
    mov pos1, si

next_first:
    inc si
    jmp find_first

prepare_second:
    mov si, 0

find_second:
    cmp si, N
    jae done
    cmp si, pos1
    je next_second     ; Exclude the first selected position, not its value

    mov bx, si
    shl bx, 1
    mov ax, A[bx]
    cmp pos2, -1
    je update_second   ; Initialize from an actual remaining element
    cmp ax, max2
    jle next_second

update_second:
    mov max2, ax
    mov pos2, si

next_second:
    inc si
    jmp find_second

done:
    ret
