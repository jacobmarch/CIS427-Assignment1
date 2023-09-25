
#include "DatabaseManager.h"
#include "ServerSocket.h"
#include "CommandHandler.h"
#include "Constants.h"
#include <iostream>

int main() {
    DatabaseManager dbManager;
    if(!dbManager.connect("pokemon_cards.db")){
        std::cerr << "Failed to create database. Exiting process." << std::endl;
        return 1;
    }
    if(!dbManager.createUsersTable()) {
        std::cerr << "Failed to create or access Users table. Exiting process." << std::endl;
        return 1;
    }
    if(!dbManager.createPokemonTable()) {
        std::cerr << "Failed to create the Pokemon_cards table. Exiting process." << std::endl;
        return 1;
    }
    //... Add other initializations if needed

    ServerSocket serverSocket;
    if(!serverSocket.initialize()) {
        std::cerr << "Failed to initialize server socket. Exiting process." << std::endl;
        return 1;
    }
    if (!serverSocket.bindSocket(SERVER_PORT)) {
        std::cerr << "Failed to bind server socket. Exiting process." << std::endl;
        return 1;
    }
    if(!serverSocket.listenSocket(1)){
        std::cerr << "Failed to set server socket to listen. Exiting process." << std::endl;
        return 1;
    }

    //CommandHandler cmdHandler(&dbManager);

    std::cout << "Server started and listening on port " << SERVER_PORT << "..." << std::endl;

    while (true) {
        int clientSocket = serverSocket.acceptConnection();
        if (clientSocket == -1){
            std::cerr << "Failed to accept client connection.";
            continue;
        }

        std::cout << "Client has established connection..." << std::endl;

        //Need to implement command handling logic as well as implementation on client + server side

        close(clientSocket);
    }

    return 0;
}
