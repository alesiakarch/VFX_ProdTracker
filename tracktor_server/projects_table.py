import sqlite3
import uuid
from sqlite3 import Error


class Projects:
    """
    Class to manage connection to the backend Projects table.

    This class provides methods to to write/read from a SQLite database directly,
    while main.py handles the requests and calls on these functions.
    
    Attributes:
        db_name (str): The name of the SQLite database file.
        connection (sqlite3.Connection or None): The database connection.
    """

    def __init__(self, db_name):
        """
        Initializes the Assets class with the database name.

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
    
    def init_project_table(self):
        """
        Creates an SQL table for projects if it doesn't already exist.
        """
        connection = self.get_db()
        connection.execute("""
                                CREATE TABLE IF NOT EXISTS projects(
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL,
                                type TEXT NOT NULL,
                                status TEXT,
                                shotsNum INTEGER,
                                deadline TEXT,
                                project_sharecode TEXT
                                )
                                """)
        connection.commit()
        connection.close()

    def get_projects(self):
        """
        Gets existing projects from db.

        Returns:
            list[sqlite3.Row]: A list of all project rows.
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM projects").fetchall()
        connection.close()
        return rows
    
    def add_project(self, name, type, status, shotsNum, deadline):
        """
        Adds a new project to projects table.

        Args:
            name (str): The name of the project.
            type (str): The type/category of the project.
            status (str): The status of the project.
            shotsNum (int): The number of shots in the project.
            deadline (str): The deadline for the project.

        Returns:
            int: The ID of the newly created project.
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
        Deletes a chosen project from project table. Note that idex won't be reset.

        Args:
            project_id (int): The ID of the project to remove.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
        connection.commit()
        connection.close()

    def get_project(self, project_id):
        """
        Returns all columns of the chosen project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            sqlite3.Row: The project row, or None if not found.
        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        connection.close()
        return row
    
    def get_sharecode(self, project_id):
        """
        Generates and/or returns a sharing code for the project with project_id.
        
        Args:
            project_id (int): The ID of the project.

        Returns:
            str: The share code for the project.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        row = cursor.execute("SELECT project_sharecode FROM projects WHERE id = ?", (project_id,)).fetchone()
        sharecode = row["project_sharecode"] if row and row["project_sharecode"] else None
        if sharecode is None:
            sharecode = str(uuid.uuid4()).split("-")[0]
            cursor.execute("UPDATE projects SET project_sharecode = ? WHERE id = ?", (sharecode, project_id))
            connection.commit()

        connection.close()
        return sharecode
    
    def get_project_id_by_sharecode(self, sharecode):
        """
        Gets the project ID associated with a given share code.

        Args:
            sharecode (str): The share code of the project.

        Returns:
            int or None: The project ID if found, otherwise None.
        """
        
        connection = self.get_db()
        row = connection.execute("SELECT id FROM projects WHERE project_sharecode = ?", (sharecode,)).fetchone()
        connection.close()
        return row["id"] if row else None

