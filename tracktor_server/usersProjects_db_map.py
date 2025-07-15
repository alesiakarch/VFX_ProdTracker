#!/usr/bin/env -S uv run --script

import sqlite3
import bcrypt
from sqlite3 import Error
from pathlib import Path


"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class UsersProjectsDBMapper:
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
        
    def init_usersProjects_table(self):
        """
        Creates and SQL table for users
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS usersProjects(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                project_id INTEGER,
                                role TEXT 
                                )
                                """,
                                )
        connection.commit()
        connection.close()

    def add_assignment(self, user_id, project_id, role):
        """
        Add a connection from a user_id to the project_id
        """
        connection = self.get_db()
        cursor = connection.cursor()


        cursor.execute("""
                       INSERT INTO usersProjects(
                       user_id,
                       project_id,
                       role
                       )
                       VALUES(?, ?, ?)
                        """, (user_id, project_id, role))
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()
        return new_id
    
    def get_assignments(self, user_id):
        """
        Get all project_ids, connected to a user_id
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT project_id FROM usersProjects WHERE user_id = ?", (user_id,))
        assignments = cursor.fetchall()
        connection.close()
        return assignments
        
    def get_all_assignments(self):
        """
        Get all user-project assignments
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM usersProjects").fetchall()
        connection.close()
        return rows

        