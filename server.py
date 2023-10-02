import socket
import threading
from command_handler import CommandHandler
from constants import SERVER_PORT


class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_handler = CommandHandler()
        self.server_running = True  # Added to control server's main loop
        self.active_clients = []  # To keep track of active client threads

    def start(self):
        self.server_socket.bind(('0.0.0.0', SERVER_PORT))
        self.server_socket.listen(1)
        print(f"Server started and listening on port {SERVER_PORT}...")

        while self.server_running:  # Change from while True to while self.server_running
            client_socket, client_address = self.server_socket.accept()
            print(f"Client {client_address} connected.")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            self.active_clients.append(client_thread)  # Add thread to active_clients list
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            command, *args = data.split()

            if command == "SHUTDOWN":
                response = self.command_handler.handle_shutdown(args)
                client_socket.send(response.encode('utf-8'))
                self.server_running = False  # Signal the main loop to stop
                for thread in self.active_clients:
                    thread.join()  # Wait for all client threads to finish
                self.shutdown()
                break
            elif command == "QUIT":
                response = self.command_handler.handle_quit(args)
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                break
            elif command == "BUY":
                response = self.command_handler.handle_buy(args)
                client_socket.send(response.encode('utf-8'))
            elif command == "SELL":
                response = self.command_handler.handle_sell(args)
                client_socket.send(response.encode('utf-8'))
            elif command == "LIST":
                response = self.command_handler.handle_list(args)
                client_socket.send(response.encode('utf-8'))
            elif command == "BALANCE":
                response = self.command_handler.handle_balance(args)
                client_socket.send(response.encode('utf-8'))
            else:
                # Unknown command handling
                response = "Unknown command."
                client_socket.send(response.encode('utf-8'))

    def shutdown(self):
        self.server_socket.close()
        print("Server has been shut down.")


if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down the server due to keyboard interrupt...")
        server.shutdown()
