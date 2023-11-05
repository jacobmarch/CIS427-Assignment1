import threading

from database_manager import DatabaseManager
from utilities import format_response, generate_error_message
from constants import CMD_BUY, CMD_SELL, CMD_LIST, CMD_LOOKUP, CMD_BALANCE, CMD_QUIT, CMD_SHUTDOWN, CMD_LOGIN, CMD_DEPOSIT, CMD_LOGOUT
import sqlite3

class CommandHandler:

    def __init__(self):
        self.db_manager = None

    def set_db_manager(self, db_manager):
        self.db_manager = db_manager

    def handle_buy(self, args):
        # Ensure that the correct number of arguments are provided
        if len(args) != 6:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 6 args.")

        pokemon_name, card_type, rarity, price_per_card, count, owner_id = args

        # Validate and convert data types of arguments
        try:
            price_per_card = float(price_per_card)
            count = int(count)
            owner_id = int(owner_id)
        except ValueError:
            return generate_error_message('INVALID_ARGUMENTS' + " Check your data types.")

        # Perform the buy operation
        success, message = self.db_manager.buy_card(pokemon_name, card_type, rarity, price_per_card, count, owner_id)
        if success:
            # Fetch updated user balance after purchase
            new_balance, new_message = self.db_manager.get_balance(owner_id)

            if new_balance is not None:
                return format_response('200 OK',
                                       f'BOUGHT: New balance: {count} {pokemon_name}. User USD balance ${new_balance}')
            else:
                return generate_error_message('DATABASE_ERROR' + " Error fetching new balance.")
        else:
            return message

    def handle_sell(self, args):
        # Extract the necessary arguments
        if len(args) != 4:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 4 args.")

        try:
            pokemon_name, quantity, card_price, owner_id = args
            quantity = int(quantity)
            card_price = float(card_price)
            owner_id = int(owner_id)
            total_earnings = card_price * quantity

            # Add card’s price to the user’s balance and update the card's table
            success, message = self.db_manager.sell_card(pokemon_name, quantity, card_price, owner_id)
            if success:
                # Fetch the updated user balance after the sale
                new_balance, bal_message = self.db_manager.get_balance(owner_id)
                if new_balance is not None:
                    return format_response('200 OK',
                                           f'SOLD: New balance: {quantity} {pokemon_name}. User’s balance USD ${new_balance}')
                else:
                    return generate_error_message('DATABASE_ERROR' + " Error fetching new balance.")
            else:
                return message
        except ValueError:
            return generate_error_message('INVALID_ARGUMENTS' + " Check your data types.")

    def handle_list(self, args):
        if len(args) != 1:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 1 arg.")

        # Extract the owner_id
        owner_id = int(args[0])
        cards, message = self.db_manager.list_cards(owner_id)

        # Check if the cards list is empty
        if not cards:
            return message

        # Formatting the cards for a response in a table format
        table_header = f"{'ID':<5}{'Card Name':<15}{'Type':<10}{'Rarity':<10}{'Count':<10}{'OwnerID':<10}"
        formatted_cards = "\n".join(
            [f"{card[0]:<5}{card[2]:<15}{card[1]:<10}{card[3]:<10}{card[4]:<10}{card[5]:<10}" for card in cards])

        return format_response('200 OK',
                               f'The list of records in the Pokémon cards table for user {owner_id}:\n{table_header}\n{formatted_cards}')

    def handle_lookup(self, args):
        if len(args) != 1:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 1 arg.")

        # Extract the card_name
        card_name = args[0]
        cards, message = self.db_manager.lookup_cards(card_name)

        # Check if the cards list is empty
        if not cards:
            return message

        # Formatting the cards for a response in a table format
        table_header = f"{'ID':<5}{'Card Name':<15}{'Type':<10}{'Rarity':<10}{'Count':<10}{'OwnerID':<10}"
        formatted_cards = "\n".join(
            [f"{card[0]:<5}{card[2]:<15}{card[1]:<10}{card[3]:<10}{card[4]:<10}{card[5]:<10}" for card in cards])

        return format_response('200 OK',
                               f'The list of records in the Pokémon cards table for {card_name} :\n{table_header}\n{formatted_cards}')
    
    def handle_balance(self, args):
        if len(args) != 1:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 1 arg.")

        # Extract the owner_id
        owner_id = int(args[0])
        balance, message = self.db_manager.get_balance(owner_id)

        # Check if balance is None (user not found or database error)
        if balance is None:
            return message

        # Fetch user details to display the name (assuming it's available in the database)
        user_details = self.db_manager.get_user_details(owner_id)

        # Check if user details exist
        if user_details is None:
            return message

        # Extract username from details
        user_name = f"{user_details[2]} {user_details[3]}"  # Assuming first_name is at index 2 and last_name is at index 3

        # Check and return balance
        return format_response('200 OK', f'Balance for user {user_name}: ${balance:.2f}')

    def handle_shutdown(self, args):
        # This will just send a response. The actual shutdown should be managed at a higher level.
        # However, we can perform some cleanup operations here, like closing the database connection.
        self.db_manager.close()
        return format_response('200 OK', 'Server shutting down...')

    def handle_quit(self, args):
        # This just sends a response. The actual disconnect will be managed by the server's socket handling.
        return format_response('200 OK', 'Goodbye!')
    
    def handle_login(self, args): 
        if len(args) != 2:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 2 args."), None

        user_name = args[0]
        password = args[1]
        # This checks to see if any users with the entered username exists, if so it takes the user's ID and password
        user_password = self.db_manager.get_password(user_name)
        
        # Check if user details exist
        if user_password[0] is None or user_password[1] is None:
            return generate_error_message('403 Wrong UserID or Password'), None
        
        # If the entered password is correct
        if user_password[0] == password:
            # user_password[1] is the ID, need to assign it to the client somehow
            return format_response('200 OK', 'Welcome!'), user_password[1]
        else:
            return generate_error_message('403 Wrong UserID or Password'), None
    
    # currently handles format 'DEPOSIT AMOUNT ID'
    # currently cannot error handle negative deposit amounts
    def handle_deposit(self, args):
        if len(args) != 2:
            return generate_error_message('MISSING_ARGUMENTS' + " This command should have 2 args.")
        
        deposit_amount, user_id = args

        # Fetch user details to display the name (assuming it's available in the database)
        user_details = self.db_manager.get_user_details(user_id)

        # Check if user details exist
        if user_details is None:
            return "USER DOES NOT EXIST"

        # Validate and convert data type of argument
        try:
            deposit_amount = float(deposit_amount)
            user_id = int(user_id)
        except ValueError:
            return generate_error_message('INVALID_ARGUMENTS' + " Check your data types.")

        # Perform deposit operation
        success, message = self.db_manager.deposit_to_account(deposit_amount, user_id)
        if success:
            # Fetch updated user balance after deposit
            new_balance, new_message = self.db_manager.get_balance(user_id)

            if new_balance is not None:
                return format_response('200 OK',
                                    f'Deposit successful. New User balance ${new_balance:.2f}')
            else:
                return generate_error_message('DATABASE_ERROR' + " Error fetching new balance.")
        else:
            return message 

    def handle_command(self, command, args):
        # A central function to delegate command handling
        handlers = {
            CMD_BUY: self.handle_buy,
            CMD_SELL: self.handle_sell,
            CMD_LIST: self.handle_list,
            CMD_LOOKUP: self.handle_lookup,
            CMD_BALANCE: self.handle_balance,
            CMD_SHUTDOWN: self.handle_shutdown,
            CMD_QUIT: self.handle_quit,
            CMD_LOGIN: self.handle_login,
            CMD_DEPOSIT: self.handle_deposit
        }

        handler = handlers.get(command)
        if handler:
            return handler(args)
        else:
            return generate_error_message('INVALID_COMMAND')
