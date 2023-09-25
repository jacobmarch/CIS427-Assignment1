
#include <netinet/in.h>

class ServerSocket {
private:
    int socketfd;
    struct socketAddressIn serverAddress;

public:
    ServerSocket();
    ~ServerSocket();

    bool initialize();
    bool bindSocket(int portNum);
    bool listenSocket(int maxConnections);
    int acceptConnection();
    void closeSocket();
};
