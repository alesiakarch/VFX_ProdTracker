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

@dataclass
class User:
    username: str
    password: str
    assigned_projects: list

@dataclass
class Project:
    name : str
    type : str
    status : str
    shotsNum : int
    deadline : str

@dataclass
class Shot:
    name : str
    duration : str # not sure what the departments need to be
    lay : str
    anim : str
    cfx : str
    lit : str
    assets : list


class DBMapper:
    """
    Class to manage connection to the backend project database. For adding projects into the db.
    """
    def __init__(self):
        """
        Initilizes the name for the application database
        """
        self.db_name = "tracktor.db" 
        self.connection = None

    def get_db(self):
        """
        Opens the named database or creates one if it doesn't exist
        """
        connection = sqlite3.connect("projects.db")
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
        return new_project
    
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
        Returns all row of the chosen project
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        connection.close()
        return row



    

