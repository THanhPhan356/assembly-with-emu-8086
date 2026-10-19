org 100h
jmp start

; Five 16-bit words per number, least significant word first.
; a = 12345678901234567890
a dw 0AD2h, 0EB1Fh, 0A98Ch, 0AB54h, 0000h

; b = 98765432109876543210
b dw 7EEAh, 0E526h, 4D38h, 5AA5h, 0005h

c dw 5 dup(0)

start:
    mov si, 2
    mov cx, 4

    ; Add the least significant words.
    mov ax, [a]
    add ax, [b]
    mov [c], ax

add_words:
    ; ADC includes the carry from the previous word.
    mov ax, [a + si]
    adc ax, [b + si]
    mov [c + si], ax

    ; INC and LOOP preserve CF; ADD SI, 2 or CMP would overwrite it.
    inc si
    inc si
    loop add_words

    int 20h
