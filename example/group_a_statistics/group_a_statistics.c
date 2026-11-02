#include <stdio.h>

int main(void)
{
    unsigned char ARR[8];
    unsigned char soluong = 0, tong = 0, max = 0, min = 9;
    unsigned char soluong_B = 0, tong_B = 0, max_B = 0, min_B = 9;
    unsigned char soluong_C = 0, tong_C = 0, max_C = 0, min_C = 9;
    int si = 0, ch;

    while (si < 8) {
        ch = getchar();
        if (ch == EOF) {
            fputs("Need eight digits.\n", stderr);
            return 1;
        }
        if (ch < '0' || ch > '9')
            continue;
        ARR[si] = (unsigned char)(ch - '0');
        ++si;
    }

    soluong = 0;
    tong = 0;
    max = 0;
    min = 9;
    si = 0;
    while (si < 8) {
        if (ARR[si] % 3 == 0) {
            ++soluong;
            tong += ARR[si];
            if (ARR[si] > max)
                max = ARR[si];
            if (ARR[si] < min)
                min = ARR[si];
        }
        ++si;
    }

    si = 0;
    soluong_B = 0;
    max_B = 0;
    min_B = 9;
    tong_B = 0;
    while (si < 8) {
        if (ARR[si] % 2 != 0 && ARR[si] % 3 != 0) {
            ++soluong_B;
            tong_B += ARR[si];
            if (ARR[si] > max_B)
                max_B = ARR[si];
            if (ARR[si] < min_B)
                min_B = ARR[si];
        }
        ++si;
    }

    si = 0;
    soluong_C = 0;
    tong_C = 0;
    max_C = 0;
    min_C = 9;
    while (si < 8) {
        if (ARR[si] % 2 == 0 && ARR[si] % 3 != 0) {
            ++soluong_C;
            tong_C += ARR[si];
            if (ARR[si] > max_C)
                max_C = ARR[si];
            if (ARR[si] < min_C)
                min_C = ARR[si];
        }
        ++si;
    }

    if (soluong == 0)
        min = 0;
    if (soluong_B == 0)
        min_B = 0;
    if (soluong_C == 0)
        min_C = 0;

    printf("%d %d %d %d %d %d %d %d %d %d %d %d\n",
           soluong, tong, max, min,
           soluong_B, tong_B, max_B, min_B,
           soluong_C, tong_C, max_C, min_C);
    return 0;
}
