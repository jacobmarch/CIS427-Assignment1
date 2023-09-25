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
            print(f"Error creating Users table: {e}")
            return False

    def create_pokemon_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pokemon_cards (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_name TEXT NOT NULL,
                    card_type TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    count INTEGER,
                    owner_id INTEGER,
                    FOREIGN KEY (owner_id) REFERENCES Users ID
                )
            """)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating Pokemon_cards table: {e}")
            return False


    #We need to add other table operations here

    def close(self):
        self.connection.close()
