#include <stdio.h>
void main() {
    char arr[32] = {87, 75, 77, 91, 76, 94, 67, 90, 74, 77, 76, 77, 75, 103, 84, 8, 78, 93, 75, 103, 90, 74, 11, 89, 83, 72, 87, 81, 86, 76, 75, 69};
    char decrypted_flag[32];

    for (int i=0; i<32; i++) {
        decrypted_flag[i] = arr[i] ^ 0x38;
    }

    printf("I decrypted the flag but now i'm going to clear it out so you can't see :)\n");
    memset(decrypted_flag, 0, 32);
    printf("bye!");

}
