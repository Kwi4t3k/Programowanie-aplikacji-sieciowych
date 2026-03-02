#include <stdio.h>

int main()
{
    float d1 = 1.5;
    float tab1[5] = {1.0,2.0,3.0,4.0,5.0};

    FILE *plik1=fopen("data.bin","wb");

    fwrite(&d1, sizeof(float), 1, plik1);
    fwrite(tab1,sizeof(float), 5, plik1);

    fclose(plik1);

    return 0;
}
