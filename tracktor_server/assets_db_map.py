#!/usr/bin/env -S uv run --script

import sqlite3
from sqlite3 import Error
from pathlib import Path


"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class AssetsDBMapper:
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
        
    def init_assets_table(self):
        """
        Creates and SQL table for users
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS assets(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                project_id INTEGER,
                                asset_name TEXT NOT NULL,
                                asset_type TEXT NOT NULL,
                                asset_status TEXT NOT NULL,
                                prepro_status TEXT NOT NULL,
                                mod_status TEXT NOT NULL,
                                srf_status TEXT NOT NULL,
                                cfx_status TEXT NOT NULL,
                                lit_status TEXT NOT NULL
                                )
                                """,
                                )
        connection.commit()
        connection.close()

    def get_assets_from_project(self, project_id):
        """
        Get assets to display on the project page
        """
        connection = self.get_db()
        asset_rows = connection.execute("SELECT * FROM assets WHERE project_id = ?", (project_id,)).fetchall()
        connection.close()
        return asset_rows
