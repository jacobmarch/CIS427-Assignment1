# CIS427-Assignment1

## Project Description
This project implements a client-server, Online Pokemon Cards Store application. The two main programs, client.py and server.py, utilize netowork sockets in the Internetdomain to communicate with each other. The client sends requests to the server, and the server sends the appropraite response back.

## Enviroment
The code is compatible with the current latest version of Python, 3.12.0. Ensure you are using Python3 on your device.

To run the code, an SHH client software, such as Bitvise for Windows, will need to be utilized. For Mac and Linux you can run the ssh client in Terminal.

## Usage
The client and server can be implemented directly in the command-line. To do this, type the following commands into 2 seperate terminals, starting with the server that will listen for client connections:

    python3 server.py
    python3 client.py

From there, you can use the BUY, SELL, LIST, BALANCE, QUIT, and SHUTDOWN commands to initiate communication with the server.

## Files Used
    client.py - implements the client, initiaties connection with server and sends requests to it
    server.py - implements the server, opens socket and listens for client connections and processes their request
    command_handler.py - handles the processing of reuqests sent to the server
    constant.py - defines constants used in code (server port numeber, command names)
    database_manager.py - interections with the SQLite database and creates the database tables
    pokemon.db - SQLite database that stores all the data (cards inventory, user records)
    utilities.py - utility functions for processing the commands, response formatting, and error handling
