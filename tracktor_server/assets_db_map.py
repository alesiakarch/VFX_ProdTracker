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
        Creates and SQL table for assets
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS assets(
                                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                project_id INTEGER,
                                asset_name TEXT NOT NULL,
                                asset_type TEXT NOT NULL,
                                asset_status TEXT NOT NULL,
                                prepro_status TEXT NOT NULL,
                                mod_status TEXT NOT NULL,
                                srf_status TEXT NOT NULL,
                                cfx_status TEXT NOT NULL,
                                lit_status TEXT NOT NULL,
                                UNIQUE(asset_name)
                                )
                                """
                                )
        connection.commit()
        connection.close()


    def add_asset_for_project(self, project_id, asset_name, asset_type):
        """
        Adds a new asset to the database
        """

        connection = self.get_db()
        cursor = connection.cursor()
        new_status = "Not Started"
        cursor.execute("""
                        INSERT INTO assets(
                        project_id,
                        asset_name,
                        asset_type,
                        asset_status,
                        prepro_status,
                        mod_status,
                        srf_status,
                        cfx_status,
                        lit_status
                       )
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                       (project_id, asset_name, asset_type, new_status, new_status, new_status, new_status, new_status, new_status))
        
        connection.commit()
        asset_id = cursor.lastrowid
        connection.close()
        return asset_id

        
    def get_assets_from_project(self, project_id):
        """
        Get assets to display on the project page
        """
        connection = self.get_db()
        asset_rows = connection.execute("SELECT * FROM assets WHERE project_id = ?", (project_id,)).fetchall()
        connection.close()
        return asset_rows
    
    def get_asset_from_project(self, project_id, asset_id):
        """
        Get all columns of one asset from one project
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM assets WHERE project_id = ? AND asset_id = ?", (project_id, asset_id)).fetchone()
        connection.close()
        return row
    
    def get_all_assets(self):
        """
        Get all existing assets
        """
        connection = self.get_db()
        assets_rows = connection.execute("SELECT * FROM assets").fetchall()
        connection.close()
        return assets_rows
    
    def remove_assets_from_project(self, project_id):
        """
        Removes all assets from the specified project
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE project_id = ?", (project_id,))
        connection.commit()
        connection.close()
    
    def remove_asset_from_project(self, asset_id):
        """
        Deletes a chosen project from project table. Note that idex won't be reset
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE asset_id=?", (asset_id,))
        connection.commit()
        connection.close()

    def change_asset_status(self, asset_id, status_item, new_status):
        """
        Changes the status of any dropdown status item, aka LAY, ANI, etc
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE assets SET {status_item} = ? WHERE asset_id = ?", (new_status, asset_id))
        connection.commit()
        connection.close()
        
