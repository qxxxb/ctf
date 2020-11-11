#include <stdio.h>

int main(int argc, char *argv[])
{
    char x = 'a';
    char f = '\a';
    x = x + f;
    printf("%c\n", x);
    return 0;
}
