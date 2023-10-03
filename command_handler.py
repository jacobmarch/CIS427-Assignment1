# -*- coding: utf-8 -*-

from database_manager import DatabaseManager
from utilities import format_response, generate_error_message
from constants import CMD_BUY, CMD_SELL, CMD_LIST, CMD_BALANCE, CMD_QUIT, CMD_SHUTDOWN

class CommandHandler:

    def __init__(self):
        self.db_manager = None

    def set_db_manager(self, db_manager):
        self.db_manager = db_manager

    def handle_buy(self, args):
        # Extract the necessary arguments
        pokemon_name, card_type, rarity, price_per_card, count, owner_id = args
        price_per_card = float(price_per_card)
        count = int(count)
        owner_id = int(owner_id)
        total_cost = price_per_card * count

        # Deduct card’s price from the user’s balance and create a new record in the card’s table
        success = self.db_manager.buy_card(owner_id, pokemon_name, card_type, rarity, price_per_card, count)
        if success:
            return format_response('200 OK',
                                   'BOUGHT: New balance: {0} {1}. User USD balance ${2}'.format(count, pokemon_name, total_cost - price_per_card * count))
        else:
            return generate_error_message('DATABASE_ERROR')

    def handle_sell(self, args):
        # Extract the necessary arguments
        pokemon_name, quantity, card_price, owner_id = args
        quantity = int(quantity)
        card_price = float(card_price)
        owner_id = int(owner_id)
        total_earnings = card_price * quantity

        # Add card’s price to the user’s balance and update the card's table
        success = self.db_manager.sell_card(owner_id, pokemon_name, quantity, total_earnings)
        if success:
            return format_response('200 OK',
                                   'SOLD: New balance: {0} {1}. User’s balance USD ${2}'.format(quantity, pokemon_name, total_earnings + card_price * quantity))
        else:
            return generate_error_message('DATABASE_ERROR')

    def handle_list(self, args):
        # Extract the owner_id
        owner_id = int(args[0])
        cards = self.db_manager.list_cards(owner_id)

        # Formatting the cards for a response
        formatted_cards = "\n".join(
            ['ID {0} Card Name {1} Type {2} Rarity {3} Count {4} OwnerID {5}'.format(card[0], card[1], card[2], card[3], card[4], card[5]) for
             card in cards])
        return format_response('200 OK',
                               'The list of records in the Pokémon cards table for current user, user {0}:\n{1}'.format(owner_id, formatted_cards))

    def handle_balance(self, args):
        # Extract the owner_id
        owner_id = int(args[0])
        balance = self.db_manager.get_balance(owner_id)

        # Fetch user details to display the name (assuming it's available in the database)
        user_details = self.db_manager.get_user_details(owner_id)
        if user_details:
            user_name = '{0} {1}'.format(user_details[2], user_details[3])  # Assuming first_name is at index 2 and last_name is at index 3
        else:
            user_name = "Unknown User"

        if balance is not None:
            return format_response('200 OK', 'Balance for user {0}: ${1}'.format(user_name, balance))
        else:
            return generate_error_message('DATABASE_ERROR')

    def handle_shutdown(self, args):
        # This will just send a response. The actual shutdown should be managed at a higher level.
        # However, we can perform some cleanup operations here, like closing the database connection.
        self.db_manager.close()
        return format_response('200 OK', 'Server shutting down...')

    def handle_quit(self, args):
        # This just sends a response. The actual disconnect will be managed by the server's socket handling.
        return format_response('200 OK', 'Goodbye!')

    def handle_command(self, command, args):
        # A central function to delegate command handling
        handlers = {
            CMD_BUY: self.handle_buy,
            CMD_SELL: self.handle_sell,
            CMD_LIST: self.handle_list,
            CMD_BALANCE: self.handle_balance,
            CMD_SHUTDOWN: self.handle_shutdown,
            CMD_QUIT: self.handle_quit
        }

        handler = handlers.get(command)
        if handler:
            return handler(args)
        else:
            return generate_error_message('INVALID_COMMAND')
