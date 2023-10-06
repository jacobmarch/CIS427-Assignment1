import socket
from constants import SERVER_PORT, CMD_QUIT, CMD_SHUTDOWN


class Client:

    def __init__(self):  # Corrected typo from __innit__ to __init__
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            #Establish connection, localhost or 127.0.0.1 for local testing
            connect_ip = input("Enter IP: ")
            self.client_socket.settimeout(1.0)
            self.client_socket.connect((connect_ip, SERVER_PORT))
            print(f"Connection established with server via port {SERVER_PORT}.")
            self.interactive_mode()
        except socket.error as e:  # Catching socket-specific errors
            print("No server to connect to.")
            print(f"Error: {e}")
        except Exception as e:  # Catching other possible exceptions
            print(f"An unexpected error occurred. Error: {e}")

    def interactive_mode(self):
        while True:
            # 1. Prompt the user for input
            command = input("Enter command (or 'quit' to disconnect): ")
            command = command.upper()

            # Exit condition for interactive mode
            if command.upper() == CMD_QUIT:
                print("Disconnecting from server...")
                break

            # 2. Send the command to the server
            self.client_socket.sendall(command.encode('utf-8'))

            # 3. Try to receive the response from the server
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                # 4. Check for error messages
                if response.startswith("ERROR:"):
                    print("Server Error:", response[6:])
                else:
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
