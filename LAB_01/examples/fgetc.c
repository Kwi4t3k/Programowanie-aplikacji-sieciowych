#include <stdio.h>

int main ()
{
    FILE *fp;
    char c;

    fp = fopen("alfabet.txt", "r");

    while ((c = fgetc(fp)) != EOF)
    {
        printf("%c", c);
    }

    fclose(fp);

    return(0);
}
