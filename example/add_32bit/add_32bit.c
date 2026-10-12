#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void) {
    uint32_t a, b, tong;
    uint8_t nho;

    printf("Nhap 2 so nguyen khong dau 32 bit: ");
    if (scanf("%" SCNu32 " %" SCNu32, &a, &b) != 2)
        return 1;

    /* Giu 32 bit thap va tach bit nho, tuong duong ban Assembly. */
    tong = a + b;
    nho = (tong < a);

    printf("Tong 32 bit = %" PRIu32 "\n", tong);
    printf("Bit nho = %u\n", (unsigned)nho);

    return 0;
}
