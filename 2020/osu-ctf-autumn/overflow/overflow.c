#include <stdio.h>
#include <stdlib.h>

#define NAME_LEN 16

/*
 * compiled with:
 * gcc -m32 -fno-stack-protector overflow.c -o overflow
 *
 */

int main(void) {
    setvbuf(stdout, 0, 2, 0); // don't buffer output

    int check = 0;
    char name[NAME_LEN];

    printf("Enter your name:\n");
    gets(name);

    if (check == 0xcafebabe) {
        printf("Welcome, %s\n", name);
        system("/bin/bash");
    } else {
        printf("Sorry %s, check value %x is incorrect.\n", name, check);
    }
}
