#!/usr/bin/env -S uv run --script

import argparse
import sqlite3
from sqlite3 import Error
import logging
from pathlib import Path
from dataclasses import dataclass

"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class UsersDBMapper:
    """
    Class to manage connection to the backend Users table
    """

    def __init__(self, db_name):
        """
        Initilizes the name for the application database
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