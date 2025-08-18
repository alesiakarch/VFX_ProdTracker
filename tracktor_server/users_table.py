import sqlite3
import bcrypt
from sqlite3 import Error

class Users:
    """
    Class to manage connection to the backend Users table.

    This class provides methods to to write/read from a SQLite database directly,
    while main.py handles the requests and calls on these functions.
    
    Attributes:
        db_name (str): The name of the SQLite database file.
        connection (sqlite3.Connection or None): The database connection.
    """
    def __init__(self, db_name):
        """
        Initializes the Assets class with the database name.

        Args:
            db_name (str): The name of the SQLite database file.
        """

        self.db_name = db_name
        self.connection = None
    
    def get_db(self):
        """
        Opens the named database or creates one if it doesn't exist.
        
        Returns:
            sqlite3.Connection: The db connection object.
        """
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = sqlite3.Row
        return connection
        
    def init_users_table(self):
        """
        Creates and SQL table for users if it doesn't already exist.
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_name TEXT NOT NULL,
                                user_password TEXT NOT NULL
                                )
                                """,
                                )
        connection.commit()
        connection.close()

    def add_user(self, username, password):
        """
        Adds a new user to the database.

        Args:
            username (str): The username for the new user.
            password (str): The plaintext password for the new user.

        Returns:
            int: The ID of the newly created user.
        """

        # hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO users(
                        user_name,
                        user_password
                       )
                       VALUES(?, ?)
                       """,
                       (username, hashed))
        
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()

        return new_id
    
    def get_user(self, user_id):
        """
        Gets user data from the table based on user_id.

        Args:
            user_id (int): The ID of the user.

        Returns:
            sqlite3.Row: The user row, or None if not found.
        """

        connection = self.get_db()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        connection.close()
        return row
    
    def get_users(self):
        """
        Gets all users from the database.

        Returns:
            list[sqlite3.Row]: A list of all user rows.
        """

        connection = self.get_db()
        rows = connection.execute("SELECT * FROM users").fetchall()
        connection.close()
        return rows
    
    def verify_user(self, username, password):
        """
        Verifies a user with username and password.

        Args:
            username (str): The username to verify.
            password (str): The plaintext password to verify.

        Returns:
            tuple: (bool, int or None). True and user ID if credentials are correct, otherwise False and None.
        """
        
        connection = self.get_db()
        row = connection.execute("SELECT user_password, id FROM users WHERE user_name = ?", (username,)).fetchone()
        connection.close()

        if row is None:
            return False, None
        stored_hash = row["user_password"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        # return True is match, overwise False
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True, row["id"]
        else:
            return False, None
        
