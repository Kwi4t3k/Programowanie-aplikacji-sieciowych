#include <sys/types.h>
#include <sys/socket.h>

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
    server_addr.sin_port = htons(port);
    inet_pton("212.182.24.27", &server_addr.sin_addr);

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1)
    {
        perror("connect");
        close(sockfd);
        return -1;
    }

    char msg[] = "Hello";

    // TCP:     send
    // UDP:     sendto

    if ((send(sockfd, msg, strlen(msg), 0) < 0))
    {
        close(sockfd);
        if (errno != 0)
        {
            perror("recv");
            exit(1);
        }
    }

    // TCP:     recv
    // UDP:     recvfrom
    char buffer[255];

    if ((recv(sockfd, buffer, 254, 0)) == 0)
    {
        if (errno != 0)
        {
            close(sockfd);
            perror("recv");
            exit(1);
        }
    }

    close(sockfd);

    return 0;
}
