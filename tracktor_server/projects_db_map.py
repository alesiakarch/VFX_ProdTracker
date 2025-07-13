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

class ProjectsDBMapper:
    """
    Class to manage connection to the backend project database. For adding projects into the db.
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
    
    def init_project_table(self):
        """
        Creates an SQL table for projects
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS projects(
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL,
                                type TEXT NOT NULL,
                                status TEXT,
                                shotsNum INTEGER,
                                deadline TEXT
                                )
                                """)
        connection.commit()
        connection.close()

    def get_projects(self):
        """
        Shows existing projects
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM projects").fetchall()
        connection.close()
        return rows
    
    def add_project(self, name, type, status, shotsNum, deadline):
        """
        Adds a new project to projects table
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO projects(
                        name,
                        type,
                        status,
                        shotsNum,
                        deadline
                        )
                        VALUES(?, ?, ?, ?, ?)
                       """,
                       (name, type, status, shotsNum, deadline)
                       )
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()

        new_project = {"id": new_id, "name": name}
        return new_id
    
    def remove_project(self, project_id):
        """
        Deletes a chosen project from project table. Note that idex won't be reset
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
        connection.commit()
        connection.close()

    def get_project(self, project_id):
        """
        Returns all columns of the chosen project
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        connection.close()
        return row