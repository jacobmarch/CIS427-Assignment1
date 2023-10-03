import sqlite3

class DatabaseManager:

    def __init__(self, db_name="pokemon_cards.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

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
            print("Error creating Users table: ", e)
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
            print("Error creating Pokemon_cards table: ", e)
            return False

    #We need to add other table operations here

    def buy_card(self, user_id, card_id, quantity, cost):
        try:
            # Decrease card count
            self.cursor.execute("UPDATE Pokemon_cards SET count = count - ? WHERE ID = ?", (quantity, card_id))

            # Decrease user balance
            self.cursor.execute("UPDATE Users SET usd_balance = usd_balance - ? WHERE ID = ?", (cost, user_id))

            # Assuming you'll have a mechanism to track which user has which cards, update that as well.
            # This is a simple approach where we just update the owner_id of the card.
            # A more scalable approach would involve a separate ownership table.
            self.cursor.execute("UPDATE Pokemon_cards SET owner_id = ? WHERE ID = ?", (user_id, card_id))

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Error buying card: ", e)
            return False

    def sell_card(self, user_id, card_id, quantity, earnings):
        try:
            # Increase card count
            self.cursor.execute("UPDATE Pokemon_cards SET count = count + ? WHERE ID = ?", (quantity, card_id))

            # Increase user balance
            self.cursor.execute("UPDATE Users SET usd_balance = usd_balance + ? WHERE ID = ?", (earnings, user_id))

            # Update card ownership (using the simple approach mentioned above)
            self.cursor.execute("UPDATE Pokemon_cards SET owner_id = NULL WHERE ID = ?", (card_id,))

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Error selling card: ", e)
            return False

    def list_cards(self, user_id=None):
        try:
            if user_id:
                # List cards owned by a specific user
                self.cursor.execute("SELECT * FROM Pokemon_cards WHERE owner_id = ?", (user_id,))
            else:
                # List all cards
                self.cursor.execute("SELECT * FROM Pokemon_cards")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error listing cards: ", e)
            return []

    def get_balance(self, user_id):
        try:
            self.cursor.execute("SELECT usd_balance FROM Users WHERE ID = ?", (user_id,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print("Error fetching balance: ", e)
            return None

    def count_users(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Users")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print("Error counting users: ", e)
            return 0

    def insert_default_user(self):
        try:
            self.cursor.execute("""
                INSERT INTO Users (email, first_name, last_name, user_name, password, usd_balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ('default@email.com', 'John', 'Doe', 'johndoe', 'password', 100.0))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Error inserting default user: ", e)

    def close(self):
        self.connection.close()
