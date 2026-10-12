#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void) {
    uint32_t a, b, sum;
    uint8_t carry;

    printf("Enter two unsigned 32-bit integers: ");
    if (scanf("%" SCNu32 " %" SCNu32, &a, &b) != 2)
        return 1;

    /* Keep the lower 32 bits and extract carry, as in the Assembly version. */
    sum = a + b;
    carry = (sum < a);

    printf("32-bit sum = %" PRIu32 "\n", sum);
    printf("Carry bit = %u\n", (unsigned)carry);

    return 0;
}
