#!/usr/bin/env -S uv run --script

import sqlite3
import datetime
from sqlite3 import Error
from pathlib import Path


class Notes:
    """
    Class to manage connection to the backend Notes table.

    This class provides methods to to write/read from a SQLite database directly,
    while main.py handles the requests and calls on these functions.
    
    Attributes:
        db_name (str): The name of the SQLite database file.
        connection (sqlite3.Connection or None): The database connection.
    """
    def __init__(self, db_name):
        """
        Initializes the Notes class with the database name.

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
    
    def init_notes_table(self):
        """
        Creates an SQL table for notes if it doesn't already exist.
        """
        connection = self.get_db()
        connection.execute("""
                            CREATE TABLE IF NOT EXISTS notes(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           item_type TEXT NOT NULL,
                           item_id INTEGER,
                           item_dept TEXT NOT NULL,
                           timestamp TEXT NOT NULL,
                           note_body TEXT NOT NULL,
                           author TEXT NOT NULL
                           )
                           """
                           )
        connection.commit()
        connection.close()

    def add_note(self, item_type, item_id, item_dept, message, user, timestamp=None ):
        """
        Creates a note to a specified item
        
        Args:
            item_type (str): The type of item (e.g., 'shot', 'asset').
            item_id (int): The ID of the item.
            item_dept (str): The department (e.g., 'LAY', 'ANI').
            message (str): The note body.
            user (str): The author of the note.
            timestamp (str): The timestamp for the note. If None, uses current time.

        Returns:
            int: The ID of the newly created note.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat(timespec='minutes')
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO notes(
                       item_type,
                       item_id,
                       item_dept,
                       timestamp,
                       note_body,
                       author
                       )
                       VALUES(?, ?, ?, ?, ?, ?)
                       """,
                       (item_type, item_id, item_dept, timestamp, message, user))
        connection.commit()
        note_id = cursor.lastrowid
        connection.close()
        return note_id
    
    def get_notes(self, item_type, item_id):
        """
        Gets all notes for the item

        Args:
            item_type (str): The type of item.
            item_id (int): The ID of the item.

        Returns:
            list[sqlite3.Row]: A list of note rows for the item.
        """
        connection = self.get_db()
        notes_rows = connection.execute("SELECT * FROM notes WHERE item_type = ? AND item_id = ?", (item_type, item_id)).fetchall()
        connection.close
        return notes_rows
    
    def get_all_notes(self):
        """
        Get all existing notes
        
        Returns:
            list[sqlite3.Row]: A list of all note rows.
        """
        connection = self.get_db()
        notes_rows = connection.execute("SELECT * FROM notes").fetchall()
        connection.close()
        return notes_rows
    
    def get_notes_for_dept(self, item_type, item_id, item_dept):
        """
        Get all notes relevant to the item's dept (LAY, ANI), etc

        Args:
            item_type (str): The type of item.
            item_id (int): The ID of the item.
            item_dept (str): The department.

        Returns:
            list[sqlite3.Row]: A list of note rows for the department.
        """

        connection = self.get_db()
        notes_rows = connection.execute("SELECT * FROM notes WHERE item_type = ? AND item_id = ? AND item_dept = ?", (item_type, item_id, item_dept)).fetchall()
        connection.close()
        return notes_rows
    
    def get_note_by_id(self, note_id):
        """
        Returns a single not by its note_id.

        Args:
            note_id (int): The ID of the note.

        Returns:
            sqlite3.Row: The note row, or None if not found.
        """

        connection = self.get_db()
        row = connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        connection.close()
        return row

