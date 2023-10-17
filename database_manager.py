import sqlite3

class DatabaseManager:

    def __init__(self, db_name="pokemon_cards.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_user_details(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE ID = ?", (user_id,))
            return self.cursor.fetchone()  # This will return None if no user is found
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def create_users_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    user_name TEXT NOT NULL,
                    password TEXT,
                    usd_balance REAL NOT NULL
                )
            """)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating Users table: {e}")
            return False

    def create_pokemon_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pokemon_cards (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_type TEXT NOT NULL,
                    card_name TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    count INTEGER,
                    owner_id INTEGER,
                    FOREIGN KEY (owner_id) REFERENCES Users(ID)
                )
            """)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating Pokemon_cards table: {e}")
            return False

    #We need to add other table operations here

    def buy_card(self, pokemon_name, card_type, rarity, price_per_card, count, owner_id):
        try:
            # Convert inputs to appropriate data types
            price_per_card = float(price_per_card)
            count = int(count)
            owner_id = int(owner_id)

            # Check if the user has sufficient balance
            self.cursor.execute("SELECT usd_balance FROM Users WHERE ID = ?", (owner_id,))
            user = self.cursor.fetchone()
            if not user or user[0] < price_per_card * count:
                return False, f"Insufficient funds or user {owner_id} does not exist"

            # Deduct price from user's balance
            self.cursor.execute("UPDATE Users SET usd_balance = usd_balance - ? WHERE ID = ?",
                                (price_per_card * count, owner_id))

            # Insert new card record into Pokemon_cards table
            self.cursor.execute("""
                INSERT INTO Pokemon_cards (card_name, card_type, rarity, count, owner_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (pokemon_name, card_type, rarity, count, owner_id))

            self.connection.commit()
            return True, None
        except ValueError:
            return False, "Invalid input: Check your data types"
        except sqlite3.Error as e:
            return False, f"Error buying card: {e}"

    def sell_card(self, pokemon_name, quantity, price_per_card, owner_id):
        try:
            # Convert inputs to appropriate data types
            price_per_card = float(price_per_card)
            quantity = int(quantity)
            owner_id = int(owner_id)
            total_earning = price_per_card * quantity

            # Fetch the existing count of the card for the user from the Pokemon_cards table
            self.cursor.execute("SELECT count FROM Pokemon_cards WHERE card_name = ? AND owner_id = ?",
                                (pokemon_name, owner_id))
            card = self.cursor.fetchone()

            # Check if the card exists and the user has enough cards to sell
            if not card or card[0] < quantity:
                return False, f"Not enough cards or card {pokemon_name} does not exist for user {owner_id}"

            # Decrease card count for the user
            self.cursor.execute("UPDATE Pokemon_cards SET count = count - ? WHERE card_name = ? AND owner_id = ?",
                                (quantity, pokemon_name, owner_id))

            # Remove the empty row if 0 cards remain
            self.cursor.execute("DELETE FROM Pokemon_cards WHERE count = 0 AND card_name = ? AND owner_id = ?",
                                (pokemon_name, owner_id))

            # Increase user balance
            self.cursor.execute("UPDATE Users SET usd_balance = usd_balance + ? WHERE ID = ?",
                                (total_earning, owner_id))

            self.connection.commit()
            return True, "Cards sold"
        except ValueError:
            return False, "Invalid input: Check your data types"
        except sqlite3.Error as e:
            return False, f"Error selling card: {e}"

    def list_cards(self, user_id=None):
        try:
            # List cards owned by a specific user
            self.cursor.execute("SELECT * FROM Pokemon_cards WHERE owner_id = ?", (user_id,))
            result = self.cursor.fetchall()
            if not result:
                return None, f"User {user_id} does not have any cards or user {user_id} does not exist"
            return result, None
        except sqlite3.Error as e:
            return [], f"Error listing cards: {e}"
        
    def lookup_cards(self, card_type=None):
        try:
            # List cards of a specific type
            self.cursor.execute("SELECT * FROM Pokemon_cards WHERE card_type = ?", (card_type,))
            result = self.cursor.fetchall()
            if not result:
                return None, f"There are no cards of {card_type} type, or {card_type} does not exist"
            return result, None
        except sqlite3.Error as e:
            return [], f"Error listing cards: {e}"

    def get_balance(self, user_id):
        try:
            self.cursor.execute("SELECT usd_balance FROM Users WHERE ID = ?", (user_id,))
            result = self.cursor.fetchone()
            if result is None:
                return None, f"No user found with {user_id}"
            return result[0], None
        except sqlite3.Error as e:
            return None, f"Error fetching balance: {e}"

    def count_users(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Users")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"Error counting users: {e}")
            return 0

    def insert_default_user(self):
        try:
            self.cursor.execute("""
                INSERT INTO Users (email, first_name, last_name, user_name, password, usd_balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ('default@email.com', 'John', 'Doe', 'johndoe', 'password', 100.0))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting default user: {e}")

    def close(self):
        self.connection.close()
