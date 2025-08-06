#!/usr/bin/env -S uv run --script

import sqlite3
from sqlite3 import Error
from pathlib import Path


"""
A mapping file to consolidate the database calls in one place, so we can swap backend from this one file
"""

class NotesDBMapper:
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
    
    def init_notes_table(self):
        """
        Creates an SQL table for notes
        """
        connection = self.get_db()
        connection.execute("""
                            CREATE TABLE IF NOT EXISTS notes(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           item_id INTEGER,
                           timestamp TEXT NOT NULL
                           note_body TEXT NOT NULL
                           author TEXT NOT NULL
                           )
                           """
                           )
        connection.commit()
        connection.close()

    def add_note(self, item_id, message, timestamp, user):
        """
        Creates a note to a specified item
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO notes(
                       item_id,
                       timestamp,
                       note_body,
                       author
                       )
                       VALUES(?, ?, ?, ?)
                       """,
                       (item_id, timestamp, message, user))
        connection.commit()
        note_id = cursor.lastrowid
        connection.close()
        return note_id
    
    def get_notes(self, item_id):
        """
        Gets all notes for the item
        """
        connection = self.get_db()
        notes_rows = connection.execute("SELECT * FROM notes WHERE item_id = ?", item_id)
        connection.close
        return notes_rows
    
    def get_all_notes(self)
        """
        Get all existing notes
        """
        connection = self.get_db
        notes_rows = connection.execute("SELECT * FROM notes")
        connection.close()
        return notes_rows