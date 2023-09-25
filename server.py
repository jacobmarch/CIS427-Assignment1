import socket
import threading
from command_handler import CommandHandler
from constants import SERVER_PORT

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_handler = CommandHandler()

    def start(self):
        # Bind the socket to the port
        self.server_socket.bind(('0.0.0.0', SERVER_PORT))
        self.server_socket.listen(5)  # Maximum of 5 pending connections
        print(f"Server started and listening on port {SERVER_PORT}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client {client_address} connected.")

            # For each client, start a new thread to handle their requests
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # Handle client requests here
        # This will involve reading data from the client, processing commands,
        # and sending responses back using the command_handler.
        pass

def shutdown(self):
    self.server_socket.close()
    # Add any other cleanup operations if needed

    if __name__ == "__main__":
        server = Server()
        try:
            server.start()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            server.shutdown()