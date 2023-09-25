
#include "DatabaseManager.h"
#include <iostream>

DatabaseManager::DatabaseManager() : db(nullptr) {}

DatabaseManager::~DatabaseManager() {
    if (db) {
        sqlite3_close(db);
    }
}

bool DatabaseManager::connect(const std::string& dbName){
    int rc = sqlite3_open(dbName.c_str(), &db);
    if (rc) {
        std::cerr << "Can't open database: " << sqlite3_errmsg(db) << std::edl;
        return false;
    } else {
        std::cout << "Opened database successfully" << std::endl;
        return true;
    }
}

bool DatabaseManager::createUsersTable() {
    //SQL to create the Users table if it doesn't exist
    const char* createUsersTable =
            "CREATE TABLE IF NOT EXISTS Users (" \
            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
            "email TEXT NOT NULL," \
            "first_name TEXT," \
            "last_name TEXT," \
            "user_name TEXT NOT NULL," \
            "password TEXT," \
            "usd_balance REAL NOT NULL" \
            ");";
    char* errorMessage = 0;
    int rc = sqlite3_exec(db, createUsersTable, 0, 0, &errorMessage);

    if (rc != SQLITE_OK) {
        std::cerr << "SQL Error: " << errorMessage << std::endl;
        sqlite3_free(errorMessage);
        return false;
    } else {
        std::cout << "Users table has been created or already exists" << std::endl;
        return true;
    }
}

bool DatabaseManager::createPokemonTable() {
    //SQL to create the Pokemon Table if it doesn't exist already
    const char* createPokemonTable =
            "CREATE TABLE IF NOT EXISTS Pokemon_cards (" \
            "ID INTEGER NOT NULL AUTO_INCREMENT," \
            "card_name TEXT NOT NULL," \
            "card_type TEXT NOT NLL," \
            "rarity TEXT NOT NULL," \
            "count INTEGER," \
            "owner_id INTEGER," \
            "PRIMARY KEY (ID)," \
            "FOREIGN KEY (owner_id) REFERENCES Users ID)" \
            ");";
    char* errorMessage = 0;
    int rc = sqlite3_exec(db, createPokemonTable, 0, 0, &errorMessage);

    if (rc != SQLITE_OK){
        std::cerr << "SQL ERROR: " << errorMessage << std::endl;
        sqlite3_free(errorMessage);
        return false;
    } else {
        std::cout << "Pokemon_cards table has been created or already exists" << std::endl;
        return true;
    }
}
