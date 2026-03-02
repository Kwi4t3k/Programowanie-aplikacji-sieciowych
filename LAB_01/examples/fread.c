#include <stdio.h>
int main()
{
    float d2, tab2[5];
    int i;

    FILE *plik2=fopen("data.bin","rb");

    fread(&d2, sizeof(float), 1, plik2);
    fread(tab2, sizeof(tab2), 1, plik2);
    fclose(plik2);

    printf("d2   = %1.2f\n", d2);

    for (i=0;i<5;i++)
       printf("%1.2f  ",tab2[i]);

    return 0;
}
