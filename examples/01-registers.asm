; Assembly with emu8086
; Exercise: observe AX, AH, AL, BH and BL.
; Expected before RET: AX = 1234h, BX = 3412h.
; Run instruction by instruction in emu8086.
; SPDX-License-Identifier: GPL-3.0-only

org 100h

mov ax, 1234h
mov bl, ah
mov bh, al

ret
