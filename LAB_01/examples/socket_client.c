#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main()
{
    int sockfd;
    struct sockaddr_in server_addr;

    // TCP:     sockfd = socket(AF_INET, SOCK_STREAM, 0)
    // UDP:     sockfd = socket(AF_INET, SOCK_DRGAM, 0)

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket");
        return -1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(22);
    inet_pton(AF_INET, "212.182.24.27", &(server_addr.sin_addr));

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1)
    {
        perror("connect");
        close(sockfd);
        return -1;
    }

    char msg[] = "Hello";

    // TCP:     send
    // UDP:     sendto

	// UDP
	// if(sendto(sockfd, msg, strlen(msg), 0, (struct sockaddr*) &server_addr, sizeof(server_addr)) < 0)

	// TCP
    if ((send(sockfd, msg, strlen(msg), 0) < 0))
    {
        close(sockfd);
        if (errno != 0)
        {
            perror("recv");
            exit(1);
        }
    }

    char buffer[255];

	// TCP:     recv
    // UDP:     recvfrom

	// UDP
    // int n_read;
    // int slen = sizeof(server_addr);
	// if((n_read = recvfrom(sockfd, buffer, SIZE, 0, (struct sockaddr *) &server_addr, &slen))< 0)

	// TCP
    if ((recv(sockfd, buffer, 254, 0)) == 0)
    {
        if (errno != 0)
        {
            close(sockfd);
            perror("recv");
            exit(1);
        }
    }

    printf("%s", buffer);

    close(sockfd);

    return 0;
}
