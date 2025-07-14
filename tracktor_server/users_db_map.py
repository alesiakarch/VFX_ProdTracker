#!/usr/bin/env -S uv run --script

import sqlite3
import bcrypt
from sqlite3 import Error
from pathlib import Path


"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class UsersDBMapper:
    """
    Class to manage connection to the backend Users table
    """

    def __init__(self, db_name):
        """
        initializes the name for the application database
        """
        self.db_name = db_name
        self.connection = None
    
    def get_db(self):
        """
        Opens the named database or creates one if it doesn't exist
        """
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = sqlite3.Row
        return connection
        
    def init_users_table(self):
        """
        Creates and SQL table for users
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
        Adds a new user to the database
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
        Gets user data from table based on user_id
        """

        connection = self.get_db()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        connection.close()
        return row
    
    def get_users(self):
        """
        Get all users
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM users").fetchall()
        connection.close()
        return rows
    
    def verify_user(self, username, password):
        """
        Verifies user with username and password
        """
        connection = self.get_db()
        row = connection.execute("SELECT user_password FROM users WHERE user_name = ?", (username,)).fetchone()
        connection.close()

        if row is None:
            return False
        stored_hash = row["user_password"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        # return True is match, overwise False
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
