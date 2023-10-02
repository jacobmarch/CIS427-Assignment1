import socket
from constants import SERVER_PORT, CMD_QUIT, CMD_SHUTDOWN


class Client:

    def __init__(self):  # Corrected typo from __innit__ to __init__
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client_socket.connect(('127.0.0.1', SERVER_PORT))
            print(f"Connection established with server via port {SERVER_PORT}.")
            self.interactive_mode()
        except Exception as e:
            print(f"Error establishing connection with server. Error: {e}")

    def interactive_mode(self):
        while True:
            # 1. Prompt the user for input
            command = input("Enter command (or 'exit' to disconnect): ")

            # Exit condition for interactive mode
            if command.upper() == CMD_QUIT:
                print("Disconnecting from server...")
                break

            # 2. Send the command to the server
            self.client_socket.sendall(command.encode('utf-8'))

            # 3. Try to receive the response from the server
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                # 4. Display the server's response to the user
                print("Server:", response)
                if response == "200 OK: Server shutting down...":
                    print("Disconnecting from server...")
                    break
            except Exception as e:
                print("Error receiving response from server:", e)
                print("You can continue to input commands or exit.")

    def shutdown(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()
    client.shutdown()
