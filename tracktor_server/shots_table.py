#!/usr/bin/env -S uv run --script

import sqlite3
from sqlite3 import Error
from pathlib import Path

class Shots:
    """
    Class to manage connection to the backend Shots table.

    This class provides methods to to write/read from a SQLite database directly,
    while main.py handles the requests and calls on these functions.
    
    Attributes:
        db_name (str): The name of the SQLite database file.
        connection (sqlite3.Connection or None): The database connection.
    """

    def __init__(self, db_name):
        """
        Initializes the Shots class with the database name.

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

    def init_shots_table(self):
        """
        Creates and SQL table for shots if it doesn't already exist.
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
        
        Args:
            project_id (int): The ID of the project.

        Returns:
            list[sqlite3.Row]: A list of shot rows for the project.
        """
        connection = self.get_db()
        shot_rows = connection.execute("""
                                        SELECT * FROM shots 
                                        WHERE project_id = ?
                                        ORDER BY CAST(SUBSTR(shot_name, 5) AS INTEGER)""", (project_id,)).fetchall()
        connection.close()
        return shot_rows
    
    def get_shot_from_project(self, project_id, shot_id):
        """
        Get all columns of one shot from one project.

        Args:
            project_id (int): The ID of the project.
            shot_id (int): The ID of the shot.

        Returns:
            sqlite3.Row: The shot row, or None if not found.
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM shots WHERE project_id = ? AND shot_id = ?", (project_id, shot_id)).fetchone()
        connection.close()
        return row
    
    def get_all_shots(self):
        """
        Get all columns of one shot from one project
        
        Returns:
            list[sqlite3.Row]: A list of all shot rows.
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM shots").fetchall()
        connection.close()
        return rows

    def add_shots_for_project(self, project_id, shotsNum):
        """
        Sends off a loop that creates a requested number of shots.

        Args:
            project_id (int): The ID of the project.
            shotsNum (int): Number of shots to create.

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

    def add_shot_for_project(self, project_id, shot_name):
        """
        Adds a single shot with a custom name to the project.

        Args:
            project_id (int): The ID of the project.
            shot_name (str): The name of the shot.

        Returns:
            int: The ID of the newly created shot.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        new_status = "Not Started"
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
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            project_id,
                            shot_name,
                            new_status,
                            new_status,
                            new_status,
                            new_status,
                            new_status
                        ))
        shot_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return shot_id

    def remove_shot_from_project(self, shot_id):
        """
        Deletes a specific shot from the database.

        Args:
            shot_id (int): The ID of the shot to remove.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM shots WHERE shot_id=?", (shot_id,))
        connection.commit()
        connection.close()
    
    def remove_shots_from_project(self, project_id):
        """
        Removes all shots from the specified project.

        Args:
            project_id (int): The ID of the project.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM shots WHERE project_id = ?", (project_id,))
        connection.commit()
        connection.close()

    def change_shot_status(self, shot_id, status_item, new_status):
        """
        Changes the status of any dropdown status item, aka LAY, ANI, etc.

        Args:
            shot_id (int): The ID of the shot.
            status_item (str): The status column to update (e.g., 'lay_status').
            new_status (str): The new status value.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE shots SET {status_item} = ? WHERE shot_id = ?", (new_status, shot_id))
        connection.commit()
        connection.close()
        

