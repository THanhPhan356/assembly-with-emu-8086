org 100h

jmp start

ARR db 1, 2, -3, 0, 4
N   dw 5
tong dw 0
dem  dw 0

start:
    mov si, 0           ; SI = index of the current element
    mov tong, 0         ; Initialize the sum
    mov dem, 0          ; Initialize the nonzero count

tinh_tong:
    cmp si, N
    jae tinh_trung_binh ; Stop when SI >= N

    mov al, ARR[si]     ; Read one signed byte
    cmp al, 0
    je bang_0          ; Skip zero elements

    cbw                ; Sign-extend AL into AX
    ; shortcut: the running sum must fit signed 16 bits; widen it for larger sums.
    add tong, ax
    inc dem            ; Count this nonzero element

bang_0:
    inc si             ; Move to the next byte
    jmp tinh_tong

tinh_trung_binh:
    xor ax, ax         ; Default result: AX = 0
    cmp dem, 0
    je ket_thuc        ; Avoid division by zero

    mov ax, tong       ; Load the signed sum
    cwd                ; Sign-extend AX into DX:AX
    mov bx, dem        ; BX = number of nonzero elements
    idiv bx            ; Signed division: quotient AX, remainder DX

ket_thuc:
    ret                ; End the COM program; keep the result in AX
