import sqlite3
from sqlite3 import Error

class Assets:
    """
    Class to manage connection to the backend Assets table.

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
        
    def init_assets_table(self):
        """
        Creates and SQL table for assets if it doesn't already exist.
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
                                lit_status TEXT NOT NULL,
                                UNIQUE(asset_name)
                                )
                                """
                                )
        connection.commit()
        connection.close()


    def add_asset_for_project(self, project_id, asset_name, asset_type):
        """
        Adds a new asset to the database.

        Args:
            project_id (int): The ID of the project.
            asset_name (str): The name of the asset.
            asset_type (str): The type of the asset.

        Returns:
            int: The ID of the newly created asset.
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
        Get assets to display on the project page.

        Args:
            project_id (int): The ID of the project.

        Returns:
            list[sqlite3.Row]: A list of asset rows for the project.

        """
        connection = self.get_db()
        asset_rows = connection.execute("SELECT * FROM assets WHERE project_id = ?", (project_id,)).fetchall()
        connection.close()
        return asset_rows
    
    def get_asset_from_project(self, project_id, asset_id):
        """
        Gets all columns of one asset from one project.

        Args:
            project_id (int): The ID of the project.
            asset_id (int): The ID of the asset.

        Returns:
            sqlite3.Row: The asset row, or None if not found.

        """
        connection = self.get_db()
        row = connection.execute("SELECT * FROM assets WHERE project_id = ? AND id = ?", (project_id, asset_id)).fetchone()
        connection.close()
        return row
    
    def get_all_assets(self):
        """
        Gets all existing assets from the db.
        
        Returns:
            list[sqlite3.Row]: A list of all asset rows.
        """
        connection = self.get_db()
        assets_rows = connection.execute("SELECT * FROM assets").fetchall()
        connection.close()
        return assets_rows
    
    def remove_assets_from_project(self, project_id):
        """
        Removes all assets from the specified project.

        Args:
            project_id (int): The ID of the project.
        """

        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE project_id = ?", (project_id,))
        connection.commit()
        connection.close()
    
    def remove_asset_from_project(self, asset_id):
        """
        Deletes a specific asset from the database.

        Args:
            asset_id (int): The ID of the asset to remove.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE id=?", (asset_id,))
        connection.commit()
        connection.close()

    def change_asset_status(self, asset_id, status_item, new_status):
        """
        Changes the status of any dropdown status item, aka LAY, ANI, etc.

        Args:
            asset_id (int): The ID of the asset.
            status_item (str): The status column to update (e.g., 'mod_status').
            new_status (str): The new status value.
        """
        connection = self.get_db()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE assets SET {status_item} = ? WHERE id = ?", (new_status, asset_id))
        connection.commit()
        connection.close()
        
