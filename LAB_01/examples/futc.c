#include <stdio.h>

int main ()
{
    FILE *fp;
    int ch;

    fp = fopen("alfabet.txt", "w+");

    for( ch = 65 ; ch <= 90; ch++ )
        fputc(ch, fp);

    fputc('\n', fp);

    for( ch = 97 ; ch <= 122; ch++ )
        fputc(ch, fp);

    fclose(fp);

    return(0);
}
