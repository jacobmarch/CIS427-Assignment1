import socket
from command_handler import CommandHandler
from constants import SERVER_PORT

class Client:

    def __innit__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client_socket.connect('0.0.0.0', SERVER_PORT)
            print(f"Connection established with server via port {SERVER_PORT}.")

        except:
            print(f"Error establishing connection with server.")

def shutdown(self):
    self.client_socket.close()