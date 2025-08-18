
import sqlite3
from sqlite3 import Error


class UsersProjects:
    """
    Class to manage connection to the backend usersProjects table.

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
        
    def init_usersProjects_table(self):
        """
        Creates and SQL table for users if it doesn't already exist.
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
        Add a connection from a user_id to the project_id.
        
        Args:
            user_id (int): The ID of the user.
            project_id (int): The ID of the project.
            role (str): The role of the user in the project.

        Returns:
            int: The ID of the newly created assignment.
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
        Get all project_ids, connected to a specific user_id.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[sqlite3.Row]: A list of project IDs for the user.
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

        Returns:
            list[sqlite3.Row]: A list of all user-project assignment rows.
        """
        connection = self.get_db()
        rows = connection.execute("SELECT * FROM usersProjects").fetchall()
        connection.close()
        return rows

        