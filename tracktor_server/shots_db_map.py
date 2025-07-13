#!/usr/bin/env -S uv run --script

import argparse
import sqlite3
from sqlite3 import Error
import logging
from pathlib import Path

"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class ShotsDBMapper:
    """
    Class to manage connection to the backend shots table
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

    def init_shots_table(self):
        """
        Creates and SQL table for shots
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS shots(
                                project_id INTEGER, 
                                shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                shot_name TEXT NOT NULL,
                                status TEXT,
                                lay_status TEXT,
                                anim_status TEXT,
                                cfx_status TEXT,
                                lit_status TEXT
                                )
                                """,
                                )
        connection.commit()
        connection.close()
    
    def get_shots_from_project(self, project_id):
        """
        Get shots to display on the project page
        """
        connection = self.get_db()
        shot_rows = connection.execute("SELECT * FROM shots WHERE project_id = ?", (project_id,)).fetchall()
        connection.close()
        return shot_rows
    
    def get_shot_from_project(self, project_id, shot_id):
        """
        Get all columns of one shot from one project
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM shots WHERE project_id = ? AND shot_id = ?", (project_id, shot_id)).fetchone()
        connection.close()
        return row
    
    def get_all_shots(self):
        """
        Get all columns of one shot from one project
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM shots").fetchall()
        connection.close()
        return rows

    def add_shots_for_project(self, project_id, shotsNum):
        """
        Sends off a loop that creates a requested number of shots
        """
        connection = self.get_db()
        cursor = connection.cursor()
        new_status ="Not Started"
        for i in range(shotsNum):
            shot_name = f"SHT_{(i+1)*10:04d}"
            cursor.execute("""
                            INSERT INTO shots(
                            project_id, 
                            shot_name,
                            status,
                            lay_status,
                            anim_status,
                            cfx_status,
                            lit_status
                           )
                           VALUES(?, ?, ?, ?, ?, ?, ?)
                           """, (project_id, 
                                 shot_name,
                                 new_status,
                                 new_status,
                                 new_status,
                                 new_status,
                                 new_status)
                            )
            connection.commit()
        connection.close()

    def remove_shots_for_project(self, project_id):
        """
        Removes all shots from the specified project
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM shots WHERE project_id = ?", (project_id,))
        connection.commit()
        connection.close()

    def change_shot_status(self, shot_id, status_item, new_status):
        """
        Changes the status of any dropdown status item, aka LAY, ANI, etc
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE shots SET {status_item} = ? WHERE shot_id = ?", (new_status, shot_id))
        connection.commit()
        connection.close()

        

