#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[])
{
    time_t t = time(0);
    srand(t);
    printf("%d\n", rand());
    return 0;
}
