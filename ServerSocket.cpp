
#include "ServerSocket.h"
#include <iostream>
#include "Constants.h"
#include <unistd.h>

ServerSocket::ServerSocket() : socketfd(-1) {
    std::memset(&serverAddress, 0, sizeof(serverAddress));
}

ServerSocket::~ServerSocket() {
    closeSocket();
}

bool ServerSocket::initialize() {
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(socketfd == -1){
        std::perror("Could not create socket");
        return false;
    }
    return true;
}

bool ServerSocket::bindSocket(int portNum) {
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(port);

    if (bind(socketfd, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == -1){
        std::perror("Binding to socket failed");
        return false;
    }
    return true;
}

bool ServerSocket::listenSocket(int maxConnections) {
    if (listen(sockfd, maxConnections) == -1) {
        std::perror("Listen failed");
        return false;
    }
    return true;
}

int ServerSocket::acceptConnection() {
    struct socketAddressIn clientAddress;
    socklen_t clientLength = sizeof(clientAddress);

    int clientSocket = accept(socketfd, (struct sockaddr*)&clientAddress, &clientLength);
    if (clientSocket == -1) {
        std::perror("Accept failed");
    }
    return clientSocket;
}

void ServerSocket::closeSocket() {
    if (socketfd != -1){
        close(socketfd);
    }
}