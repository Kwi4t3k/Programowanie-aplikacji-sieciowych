#include <stdio.h>

int main ()
{
    FILE * fp;

    int n = 2017;
    char text[] = "Programowanie w jezyku C.\n";
    double pi = 3.14;

    fp = fopen ("myfile.txt","w");

    fprintf (fp, "%d\n", n);
    fprintf (fp, "%lf\n", pi);
    fprintf (fp, "%s\n", text);

    fclose (fp);

    return 0;
}
