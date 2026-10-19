#include <stdint.h>
#include <stdio.h>

int main(void) {
    /* Five 16-bit words per number, least significant word first. */
    uint16_t a[5] = {0x0AD2, 0xEB1F, 0xA98C, 0xAB54, 0x0000};
    uint16_t b[5] = {0x7EEA, 0xE526, 0x4D38, 0x5AA5, 0x0005};
    uint16_t c[5];
    uint32_t total, carry = 0;
    int i;

    for (i = 0; i < 5; i++) {
        total = (uint32_t)a[i] + b[i] + carry;
        c[i] = (uint16_t)total;
        carry = total >> 16;
    }

    printf("Sum (16-bit words, low first):");
    for (i = 0; i < 5; i++)
        printf(" %04X", (unsigned)c[i]);
    putchar('\n');

    return 0;
}
