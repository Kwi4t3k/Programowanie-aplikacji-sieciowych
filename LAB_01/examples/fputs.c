#include <stdio.h>

int main ()
{
   FILE *fp;

   fp = fopen("file.txt", "w+");

   fputs("This is c programming.\n", fp);
   fputs("This is a system programming language.\n", fp);
   fputs("We are programming in C in 2017 year.\n", fp);
   fputs("Today is 26.01.2017", fp);

   fclose(fp);

   return(0);
}
