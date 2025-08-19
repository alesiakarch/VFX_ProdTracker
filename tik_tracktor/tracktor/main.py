"""
Main module for Tracktor integration.
This file is based on the original integration of Kitsu and Shotgrid made by the TIK Manager team.
"""
from tik_manager4.management.management_core import ManagementCore
from tik_manager4.core.constants import DataTypes 
from tik_manager4.external.tracktor.tracktor_api import TracktorAPI
from tik_manager4.management.tracktor.ui.login import Login
from pathlib import Path

# add external folder with extra dependencies if needed
print("tracktor/main.py loaded")

class ProductionPlatform(ManagementCore):
    """
    Main class for Tracktor integration.

    Handles authentication, project synchronization, and asset/shot management
    between Tik Manager and the Tracktor backend.

    Some methods are left unimplemented, since they aren't supported by current Tracktor's functionality
    but are required by the TIK's ManagementCore.

    Attributes:
        tik_main: The main Tik Manager object.
        api (TracktorAPI or None): The Tracktor API client instance.
        is_authenticated (bool): Whether the user is authenticated.
        user (str or None): The username of the authenticated user.
    """

    metadata_pairing = {
        "start_fr": "start_frame",
        "end_fr": "end_frame",
        "fps": "fps",
    }

    nice_name = "Tracktor VFX"
    name = "tracktor"
    lock_subproject_creation = True
    lock_task_creation = True

    def __init__(self, tik_main_obj):
        """
        Initializes the ProductionPlatform instance.

        Args:
            tik_main_obj: The main Tik Manager object.
        """
        self.tik_main = tik_main_obj
        self.api = None # not connected to Tracktor yet
        self.is_authenticated = False # user isn't logged in yet
        self.user = None # no user data at the init
        print("Tracktor ProductionPlatform instantiated")
        super().__init__()

    @property
    def host(self):
        """
        Returns the Tracktor host URL from Tik Manager settings.

        Returns:
            str: The Tracktor host URL.
        """
        return self.tik_main.user.commons.management_settings.get("tracktor_url")
    
    @property
    def host_api(self):
        """
        Returns the Tracktor API base URL.

        Returns:
            str: The Tracktor API base URL.
        """
        host = self.host
        
        if host.endswith("/"):
            host = host[:-1]
        return f"{host}/api"
        
    def authenticate(self):
        """
        Authenticates the user in Tracktor.

        Returns:
            tuple: (TracktorAPI instance or None, str message)

        Raises:
            Exception: shows an error if authentication failed.
        """

        login_widget = Login(TracktorAPI)
        ret = login_widget.exec_()
        if not ret:
            return None, "Canceled by user."
        user = login_widget.inputs["user"].text()
        password = login_widget.inputs["password"].text()
        host = login_widget.inputs["host"].text()

        self.tracktor_username = user
        self.tracktor_password = password
        self.tracktor_host = host

        self.api = TracktorAPI(host, user, password)
        try:
            self.api.login()
            self.is_authenticated = True
            self.user = user
            return self.api, "Authenticated"
        
        except Exception as e:
            self.api = None
            self.is_authenticated = False
            self.user = None
            return None, f"Authentication failed: {e}"
                
    def logout(self):
        """
        Logs out the user from Tracktor and clears credentials.
        """

        if self.api:
            try:
                self.api.logout()
            except:
                pass
        self.api = None
        self.is_authenticated = False
        self.user = None
        if hasattr(self, "tracktor_username"):
            del self.tracktor_username
        if hasattr(self, "tracktor_password"):
            del self.tracktor_password

    def get_projects(self):
        """
        Retrieves a list of projects from Tracktor.

        Returns:
            list: A list of project dictionaries.

        Raises:
            Exception: If not authenticated.
        """
        
        if not self.api:
            raise Exception("Not authenticated")
        return self.api.get_projects()

    def create_from_project(self, project_root, tracktor_project_id, set_project=True):
        """
        Creates a Tik Manager project from a Tracktor project.

        Args:
            project_root: The root directory for the new project.
            tracktor_project_id (int): The Tracktor project ID.
            set_project (bool): Whether to set the new project as active. Defaults to True.

        Returns:
            Path or None: The path to the created project, or None if creation failed.
        """

        print("create_from_project called")
        sync_stamp = self.date_stamp()
        print(f"sync_stamp: {sync_stamp}")

        # get tiks project path
        current_project_path = self.tik_main.project.absolute_path
        print(f"current_project_path: {current_project_path}")

        print(f"Fetching project from Tracktor: {tracktor_project_id}")
        project = self.api.get_project(tracktor_project_id)
        print(f"Project fetched: {project}")

        project_name = project["name"]
        print(f"Project name: {project_name}")

        project_path = Path(project_root) / project_name
        print(f"Project path to create: {project_path}")

        project_path.mkdir(exist_ok=True)
        print(f"Directory created (or already exists): {project_path}")

        print("Calling tik_main.create_project...")
        ret = self.tik_main.create_project(
            project_path.as_posix(), structure_template="empty",
            set_after_creation=True
        )
        print(f"tik_main.create_project returned: {ret}")

        if ret == -1:
            print("Project creation failed (ret == -1)")
            return None

        print("Project creation succeeded")

        # Fetch all assets and shots from Tracktor
        all_assets = self.api.get_assets(tracktor_project_id)
        all_shots = self.api.get_shots(tracktor_project_id)

        print("Fetched assets and shots")

        # Get or create the 'Assets' and 'Shots' subprojects
        assets_sub = self._get_assets_sub()
        shots_sub = self._get_shots_sub()

        print("Created assets and shots subproject")

        # Sync assets (no categories)
        for asset in all_assets:
            self._sync_new_asset(asset, assets_sub, [])

        # Sync shots (no categories)
        for shot in all_shots:
            self._sync_new_shot(shot, shots_sub, [])

        print("Synced shots and assets")

        # Tag the project as management driven
        self.tik_main.project.settings.edit_property("management_driven", True)
        self.tik_main.project.settings.edit_property("management_platform", "tracktor")
        self.tik_main.project.settings.edit_property("host_project_name", project["name"])
        self.tik_main.project.settings.edit_property("host_project_id", tracktor_project_id)
        self.tik_main.project.settings.edit_property("last_sync", sync_stamp)
        self.tik_main.project.settings.apply_settings(force=True)

        if not set_project:  # switch back to the original project
            self.tik_main.set_project(current_project_path)

        return project_path

    def _sync_new_asset(self, asset_data, assets_sub, asset_categories):
        """
        Syncs a new asset from Tracktor.

        Args:
            asset_data (dict): Asset data from Tracktor.
            assets_sub: The Tik Manager assets subproject.
            asset_categories (list): List of asset categories.

        Returns:
            Task: The created Tik Manager task for the asset.
        """
        asset_id = asset_data["id"]
        asset_name = asset_data["asset_name"]

        sub = assets_sub
        sub.add_task(asset_name, categories=["MOD", "SRF", "RIG", "CFX", "LIT"], uid=asset_id)
        task = sub.tasks[asset_name]
    
        task.edit_property("tracktor_asset_type", asset_data["asset_type"])
        task.edit_property("tracktor_asset_status", asset_data["asset_status"])
        task.apply_settings(force=True)
        return task
    
    def _sync_new_shot(self, shot_data, shots_sub, shot_categories):
        """
        Syncs a new shot from Tracktor.

        Args:
            shot_data (dict): Shot data from Tracktor.
            shots_sub: The Tik Manager shots subproject.
            shot_categories (list): List of shot categories.

        Returns:
            Task: The created Tik Manager task for the shot.
        """

        shot_id = shot_data["shot_id"]
        shot_name = shot_data["shot_name"]
        sub = shots_sub
        
        task = sub.add_task(shot_name, categories=["LAY", "ANI", "CFX", "LIT"], uid=shot_id)
        print("DEBUG: sub.tasks keys after add_task:", list(sub.tasks.keys()))
        # task = sub.tasks[shot_name]
        # Optionally, add more Tracktor fields as metadata:

        return task
    
    def _get_assets_sub(self):
        """
        Gets or creates the 'Assets' subproject in Tik Manager.

        Returns:
            SubProject: The assets subproject.
        """

        assets_sub = self.tik_main.project.subs.get("Assets") or self.tik_main.project.create_sub_project(
            "Assets", parent_path="", mode="asset"
        )
        return assets_sub

    def _get_shots_sub(self):
        """
        Gets or creates the 'Shots' subproject in Tik Manager.

        Returns:
            SubProject: The shots subproject.
        """

        shots_sub = self.tik_main.project.subs.get("Shots") or self.tik_main.project.create_sub_project(
            "Shots", parent_path="", mode="shot"
        )
        return shots_sub
    
    def force_sync(self):
        """
        Forcefully synchronizes the current Tik Manager project with Tracktor.

        Is a duplicate of the sync_project() function because of the ProductionPlatform inheritance

        Returns:
            tuple: (bool, str) indicating success and a message.
        """
        return self.sync_project()
    
    def sync_project(self):
        """
        Synchronizes the Tik Manager project with Tracktor.

        Returns:
            tuple: (bool, str) indicating success and a message.
        """
        
        sync_stamp = self.date_stamp()

        project_id = self.tik_main.project.settings.get("host_project_id")

        if not project_id:
            return False, "Project is not linked to a Tracktor project."

        management_platform = self.tik_main.project.settings.get("management_platform")
        if management_platform != "tracktor":
            return False, "Project is not linked to a Tracktor project."

        # 1. Fetch current assets/shots from Tracktor
        tracktor_assets = self.api.get_assets(project_id)
        tracktor_shots = self.api.get_shots(project_id)
        tracktor_asset_names = {asset["asset_name"] for asset in tracktor_assets}
        tracktor_shot_names = {shot["shot_name"] for shot in tracktor_shots}

        # 2. Fetch current assets/shots from Tik
        assets_sub = self._get_assets_sub()
        shots_sub = self._get_shots_sub()
        tik_assets = assets_sub.tasks
        tik_shots = shots_sub.tasks
        tik_asset_names = set(tik_assets.keys())
        tik_shot_names = set(tik_shots.keys())

        asset_categories = ["MOD", "SRF", "RIG", "CFX", "LIT"]
        shot_categories = ["LAY", "ANI", "CFX", "LIT"]
        # 3. Add new assets/shots from Tracktor
        for asset in tracktor_assets:
            if asset["asset_name"] not in tik_asset_names:
                self._sync_new_asset(asset, assets_sub, asset_categories)
        for shot in tracktor_shots:
            print(["shot_name"])
            if shot["shot_name"] not in tik_shot_names:
                self._sync_new_shot(shot, shots_sub, shot_categories)

        # 5. (Optional) Update changed assets/shots
        # You can compare fields and update Tik if needed

        self.tik_main.project.settings.edit_property("last_sync", sync_stamp)
        self.tik_main.project.settings.apply_settings(force=True)

        return True, "Success"
        
    def get_all_assets(self):
        """This method is called when all assets are retrieved."""
        raise NotImplementedError("The method 'get_all_assets' must be implemented.")

    def get_all_shots(self):
        """This method is called when all shots are retrieved."""
        raise NotImplementedError("The method 'get_all_shots' must be implemented.")

    def get_entity_url(self, entity_type, entity_id):
        """This method is called when the URL of an entity is retrieved."""
        raise NotImplementedError("The method 'get_entity_url' must be implemented.")

    def request_tasks(self, entity_id, entity_type, step=None, project_id=None):
        """This method is called when tasks are requested."""
        raise NotImplementedError("The method 'request_tasks' must be implemented.")

    def get_available_status_lists(self, force=False):
        """This method is called when the available status lists are retrieved."""
        raise NotImplementedError("The method 'get_available_status_lists' must be implemented.")

    def publish_version(self, *args, **kwargs):
        """This method is called when a version is published."""
        raise NotImplementedError("The method 'publish_version' must be implemented.")

    @staticmethod # sets settings 
    def get_settings_ui():
        """
        Returns the UI settings for the Tracktor platform.

        Returns:
            dict: A dictionary of settings UI configuration.
        """

        # Make sure the keys are unique across all other platforms
        return {
            "_tracktor_blank": {
                "display_name": "",
                "value": "--------------------------------------------------------",
                "type": DataTypes.INFO.value,
                "font_size": 12,
            },
            "_tracktor": {
                "display_name": "",
                "type": DataTypes.INFO.value,
                "value": "Tracktor Settings",
                "font_size": 14,
                "bold": True,
            },
            "tracktor_url": {
                "display_name": "Tracktor Host URL",
                "tooltip": "The URL of the Tracktor server to connect to.",
                "type": DataTypes.STRING.value,
                "value": "",
            }
        }

