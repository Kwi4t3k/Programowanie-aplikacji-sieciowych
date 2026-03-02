#include <stdio.h>

int main ()
{
    FILE *fp;
    char bufor[1024];

    fp = fopen("data.txt", "r");

    while(fscanf(fp, "%s", bufor))
    {
        printf("%s\n", bufor);

        if(feof(fp))
            break;
    }

    fclose(fp);

    return 0;
}
