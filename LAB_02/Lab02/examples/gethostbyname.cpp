#include<stdio.h> //printf
#include<string.h> //memset
#include<stdlib.h> //for exit(0);
#include<sys/socket.h>
#include<errno.h> //For errno - the error number
#include<netdb.h> //hostent
#include<arpa/inet.h>
#include <string>
#include <iostream>

int main(int argc , char *argv[])
{
    std::string hostname = "www.umcs.pl";
    char IP[255];

    struct hostent *h;
    struct in_addr **addrlist;

    if((h = gethostbyname(hostname.c_str())) == NULL)
        exit(-1);

    addrlist = (struct in_addr**) h->h_addr_list;
    strcpy(IP, inet_ntoa(*addrlist[0]));

    std::cout << IP << "\n";

    return 0;

}
