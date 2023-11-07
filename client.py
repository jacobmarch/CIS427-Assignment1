import socket
import threading
from constants import SERVER_PORT, CMD_QUIT, CMD_SHUTDOWN


def clear_current_line():
    # ANSI escape sequence to move the cursor to the beginning of the line and clear the line
    print('\r', end='')  # Return to the start of the line
    print(' ' * (len("Enter command (or 'quit' to disconnect): ") + 20), end='')  # Overwrite the line with spaces
    print('\r', end='')  # Return to the start of the line again


class Client:

    def __init__(self):  # Corrected typo from __innit__ to __init__
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_response_listener = threading.Thread(target=self.listen_for_server_responses)
        self.running = True

    def listen_for_server_responses(self):
        while self.running:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if not response:
                    print("\nServer connection has been closed.")
                    self.stop()
                    break

                print("\nServer:", response)
                # Check for the server's shutdown message
                if response.startswith("200 OK: Server shutting down"):
                    print("\nServer is shutting down. Disconnecting...")
                    self.stop()
                    break

            except socket.error as e:
                print("\nConnection to server lost:", e)
                self.stop()
                break
            except Exception as e:
                print("\nAn unexpected error occurred:", e)
                self.stop()
                break

    def start(self):
        try:
            #Establish connection, localhost or 127.0.0.1 for local testing
            connect_ip = input("Enter IP: ")
            self.client_socket.connect((connect_ip, SERVER_PORT))
            print(f"Connection established with server via port {SERVER_PORT}.")
            self.server_response_listener.start()
            self.interactive_mode()
        except socket.error as e:  # Catching socket-specific errors
            print("No server to connect to.")
            print(f"Error: {e}")
        except Exception as e:  # Catching other possible exceptions
            print(f"An unexpected error occurred. Error: {e}")

    def stop(self):
        self.running = False
        try:
            # Attempt to close the socket gracefully
            self.client_socket.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            # Ignore the error since we're stopping the client anyway
            pass
        finally:
            self.client_socket.close()
            print("Client stopped.")

    def interactive_mode(self):
        while self.running:
            command = input("Enter command (or 'quit' to disconnect): ")
            if not self.running:
                # If the server has shutdown, exit the loop immediately
                break
            if command.lower() == 'quit' or command.lower() == 'shutdown':
                self.send_command(command)
                break
            self.send_command(command)

    def send_command(self, command):
        try:
            self.client_socket.sendall(command.encode('utf-8'))
        except socket.error as e:
            print("Error sending command:", e)
            self.stop()

    def shutdown(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()
