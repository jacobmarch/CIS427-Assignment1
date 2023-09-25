
#include <sqlite3.h>
#include <string>

class DatabaseManager {
private:
    sqlite3* db;

public:
    DatabaseManager();
    ~DatabaseManager();

    bool connect(const std::string& dbName);
    bool createUsersTable();
    bool createPokemonTable();
};



