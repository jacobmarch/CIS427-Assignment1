import socket
import threading
from command_handler import CommandHandler
from constants import SERVER_PORT, CMD_QUIT, CMD_SHUTDOWN, CMD_LIST, CMD_LOOKUP, CMD_BALANCE, CMD_SELL, CMD_BUY, CMD_LOGIN, CMD_DEPOSIT, CMD_LOGOUT, CMD_WHO
from database_manager import DatabaseManager

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_handler = CommandHandler()
        self.server_running = True  # Added to control server's main loop
        self.active_clients = []  # To keep track of active client threads
        self.db_manager = DatabaseManager()
        self.db_manager.create_users_table()
        self.db_manager.create_pokemon_table()
        self.client_user_map = {}

    @staticmethod
    def setup_database():
        db_manager = DatabaseManager()

        db_manager.create_users_table()
        db_manager.create_pokemon_table()
        if db_manager.count_users() == 0:
            db_manager.insert_default_user()
            print("Inserted default users into the Users table.")
        db_manager.close()

    def start(self):
        self.setup_database()
        self.server_socket.bind(('0.0.0.0', SERVER_PORT))
        self.server_socket.listen(10)
        print(f"Server started and listening on port {SERVER_PORT}...")

        while self.server_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Client {client_address} connected.")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                self.active_clients.append(client_thread)  # Add thread to active_clients list
                client_thread.start()
            except OSError as e:
                if not self.server_running:
                    print("Server offline.")
                else:
                    print(f"Unexpected error occurred: {e}")

    def thread_id(self, user_id):
        thread_id = threading.get_ident()
        self.client_user_map[thread_id] = user_id

    def handle_client(self, client_socket):
        try:
            db_manager = DatabaseManager()
            self.command_handler.set_db_manager(db_manager)

            while True:
                data = client_socket.recv(1024).decode('utf-8')
                print(f'Client Command: {data}')
                if not data:
                    break

                command, *args = data.split()

                thread_id = threading.get_ident()
                user_id = self.client_user_map.get(thread_id)
                

                if command == CMD_LOGIN:
                    response, user_id = self.command_handler.handle_login(args)
                    client_socket.send(response.encode('utf-8'))
                    if response.startswith("200 OK"):
                        self.thread_id(user_id)
                elif command == CMD_SHUTDOWN:
                    response = self.command_handler.handle_shutdown(args)
                    client_socket.send(response.encode('utf-8'))
                    self.server_running = False  # Signal the main loop to stop
                    for thread in self.active_clients:
                        if thread is not threading.current_thread():
                            thread.join()  # Wait for all client threads to finish
                        self.shutdown()
                        break
                elif command == CMD_QUIT:
                    response = self.command_handler.handle_quit(args)
                    client_socket.send(response.encode('utf-8'))
                    client_socket.close()
                    break
                elif command == CMD_BUY:
                    response, _ = self.command_handler.handle_buy(args, user_id)
                    client_socket.sendall(response.encode('utf-8'))
                elif command == CMD_SELL:
                    response, _ = self.command_handler.handle_sell(args, user_id)
                    client_socket.sendall(response.encode('utf-8'))
                elif command == CMD_LIST:
                    response = self.command_handler.handle_list(args, user_id)
                    client_socket.send(response.encode('utf-8'))
                elif command == CMD_LOOKUP:
                    response, _ = self.command_handler.handle_lookup(args, user_id)
                    client_socket.send(response.encode('utf-8'))
                elif command == CMD_BALANCE:
                    response = self.command_handler.handle_balance(args, user_id)
                    client_socket.send(response.encode('utf-8'))
                elif command == CMD_DEPOSIT:
                    # Implement deposit command
                    if user_id is not None:
                        response = self.command_handler.handle_deposit(args, user_id)
                        client_socket.send(response.encode('utf-8'))
                    # If user is not logged in
                    else:
                        response = "403 ERROR: You must be logged in to perform this action."
                        client_socket.send(response.encode('utf-8'))
                elif command == CMD_LOGOUT:
                    thread_id = threading.get_ident()
                    if thread_id in self.client_user_map:
                        # Log out the user by deleting the mapping
                        user_id = self.client_user_map[thread_id]
                        del self.client_user_map[thread_id]
                        response = '200 OK ' + f'User {user_id} logged out successfully'
                        client_socket.send(response.encode('utf-8'))
                    else:
                        # If no user is logged in on this thread, return an error
                        response = 'You are not logged in'
                        client_socket.send(response.encode('utf-8'))
                elif command == CMD_WHO:
                    if user_id is not None:
                        response = self.command_handler.handle_who(args, user_id, self.client_user_map)
                        client_socket.send(response.encode('utf-8'))
                    else:
                        response = "403 ERROR: You must be logged in as root to perform this action."
                        client_socket.send(response.encode('utf-8'))
                else:
                    # Unknown command handling
                    response = "400 ERROR: Unknown command."
                    client_socket.send(response.encode('utf-8'))

            else:
                print('You must login to access the database')

            db_manager.close()
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

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
