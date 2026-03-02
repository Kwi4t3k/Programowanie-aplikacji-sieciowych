#include <stdio.h>

int main ()
{
    FILE *fp;
    char bufor[1024];

    fp = fopen("Untitled3.c", "r");

    while(!feof(fp))
    {
        if(fscanf(fp, "%s", bufor) != 1)
            break;

        printf("%s\n", bufor);
    }

    fclose(fp);

    return 0;
}
