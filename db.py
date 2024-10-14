import sqlite3

class DatabaseConnection:
    _instance = None

    def __new__(cls, db_file):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_file)
            cls._instance.connection.row_factory = sqlite3.Row
        return cls._instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self._instance = None

    def init_db(self):
        cursor = self.connection.cursor()

        initial_sql_profile = ("Create table if not exists profiles (id INTEGER PRIMARY KEY, profile_name TEXT,"
                               "module_index INTEGER, module_name TEXT, email TEXT, password TEXT, recovery_email TEXT,"
                               "proxy_ip TEXT, proxy_port TEXT, proxy_username TEXT, proxy_password TEXT)")
        cursor.execute(initial_sql_profile)
        self.connection.commit()
        cursor.close()
