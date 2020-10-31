#include <stdio.h>
#include <stdlib.h>

#define Hauptroutine main
#define nichts void
#define int int
#define schleife(n) for (int i = n; i--;)
#define bitrverschieb(n, m) (n) >> (m)
#define diskreteAddition(n, m) (n) ^ (m)
#define wenn if
#define ansonsten else
#define Zeichen char
#define Zeiger *
#define Referenz &
#define Ausgabe(s) puts(s)
#define FormatAusgabe printf
#define FormatEingabe scanf
#define Zufall rand()
#define istgleich =
#define gleichbedeutend ==

int main(void) {
    int i = rand();
    int k = 13;
    int e;
    int* p = &i;

    printf("%d\n", i);
    fflush(stdout);
    scanf("%d %d", &k, &e);

    for (int i = 7; i--;)
        k = (*p) >> (k % 3);

    k = k ^ e;

    if(k == 53225)
        puts("Success");
    else
        puts("Fail");

    return 0;
}
