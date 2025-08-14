"""Main module for Tracktor integration."""
from tik_manager4.management.management_core import ManagementCore
from tik_manager4.core.constants import DataTypes 
from tik_manager4.external.tracktor.tracktor_api import TracktorAPI
from tik_manager4.management.tracktor.ui.login import Login
from pathlib import Path

# add external folder with extra dependencies if needed
print("tracktor/main.py loaded")

class ProductionPlatform(ManagementCore):
    """Main class for Tracktor integration."""

    metadata_pairing = {
        "start_fr": "start_frame",
        "end_fr": "end_frame",
        "fps": "fps",
    }

    nice_name = "Tracktor VFX"
    name = "tracktor"
    lock_subproject_creation = True
    lock_task_creation = True

# TIK manager code copy start
    def __init__(self, tik_main_obj):
        self.tik_main = tik_main_obj
        self.api = None # not connected to Tracktor yet
        self.is_authenticated = False # user isn't logged in yet
        self.user = None # no user data at the init
        print("Tracktor ProductionPlatform instantiated")
        super().__init__()

    @property
    def host(self):
        return self.tik_main.user.commons.management_settings.get("tracktor_url")
    
    @property
    def host_api(self):
        host = self.host
        # if it is ending with a slash, remove it
        if host.endswith("/"):
            host = host[:-1]
        return f"{host}/api"
    
# End of TIK code
        
    def authenticate(self):
        """Authenticate the user."""
        # Show login dialog if credentials are missing or invalid
        login_widget = Login(TracktorAPI)
        ret = login_widget.exec_()
        if not ret:
            return None, "Canceled by user."
        user = login_widget.inputs["user"].text()
        password = login_widget.inputs["password"].text()
        host = login_widget.inputs["host"].text()
        # Store credentials
        self.tracktor_username = user
        self.tracktor_password = password
        self.tracktor_host = host
        # Authenticate
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
        """Return a list of projects from Tracktor."""
        if not self.api:
            raise Exception("Not authenticated")
        return self.api.get_projects()

    def sync_project(self):
        """This method is called when the project is synced."""
        raise NotImplementedError("The method 'sync_project' must be implemented.")

    def force_sync(self):
        """This method is called when the project is forcefully synced."""
        raise NotImplementedError("The method 'force_sync' must be implemented.")

    def create_from_project(self, project_root, tracktor_project_id, set_project=True):
        """Create a tk manager project from a tracktor project."""
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
        Sync a new asset from Tracktor.
        asset_data: dict with keys 'id', 'asset_name', 'asset_type', etc.
        """
        asset_id = asset_data["id"]
        asset_name = asset_data["asset_name"]
        # If you want to organize by asset_type, you can do so here:
        # asset_type = asset_data["asset_type"]
        # sub = assets_sub.subs.get(asset_type) or assets_sub
        # Otherwise, just use assets_sub:
        sub = assets_sub
        task = sub.add_task(asset_name, categories=["MOD", "SRF", "RIG", "CFX", "LIT"], uid=asset_id)
        # Optionally, add more Tracktor fields as metadata:
        task.edit_property("tracktor_asset_type", asset_data["asset_type"])
        task.edit_property("tracktor_asset_status", asset_data["asset_status"])
        # ...add other fields as needed...
        task.apply_settings(force=True)
        return task
    
    def _sync_new_shot(self, shot_data, shots_sub, shot_categories):
        """
        Sync a new shot from Tracktor.
        shot_data: dict with keys 'shot_id', 'shot_name', etc.
        """
        shot_id = shot_data["shot_id"]
        shot_name = shot_data["shot_name"]
        sub = shots_sub
        task = sub.add_task(shot_name, categories=["LAY", "ANI", "CFX", "LIT"], uid=shot_id)
        # Optionally, add more Tracktor fields as metadata:
        task.edit_property("tracktor_status", shot_data["status"])
        # ...add other fields as needed...
        task.apply_settings(force=True)
        return task
    
    def _get_assets_sub(self):
        """Get the 'Assets' sub from the tik project.

        Creates if it doesn't exist.
        """
        # TODO: should go to the base class
        assets_sub = self.tik_main.project.subs.get("Assets") or self.tik_main.project.create_sub_project(
            "Assets", parent_path="", mode="asset"
        )
        return assets_sub

    def _get_shots_sub(self):
        """Get the 'Shots' sub from the tik project.

        Creates if it doesn't exist.
        """
        # TODO: should go to the base class
        shots_sub = self.tik_main.project.subs.get("Shots") or self.tik_main.project.create_sub_project(
            "Shots", parent_path="", mode="shot"
        )
        return shots_sub
    
    def force_sync(self, project_id=None):
        """
        Sync Tik Manager project with Tracktor project.
        - Add new assets/shots from Tracktor
        - Remove assets/shots in Tik that no longer exist in Tracktor
        - Update changed assets/shots
        """
        sync_stamp = self.date_stamp()
        project_id = project_id or self.tik_main.project.settings.get("host_project_id")
        if not project_id:
            LOG.error("Project is not linked to a Tracktor project.")
            return False, "Project is not linked to a Tracktor project."

        management_platform = self.tik_main.project.settings.get("management_platform")
        if management_platform != "tracktor":
            LOG.error("Project is not linked to a Tracktor project.")
            return False, "Project is not linked to a Tracktor project."

        # 1. Fetch current assets/shots from Tracktor
        tracktor_assets = self.api.get_assets(project_id)
        tracktor_shots = self.api.get_shots(project_id)
        tracktor_asset_names = {a["asset_name"] for a in tracktor_assets}
        tracktor_shot_names = {s["shot_name"] for s in tracktor_shots}

        # 2. Fetch current assets/shots from Tik
        assets_sub = self._get_assets_sub()
        shots_sub = self._get_shots_sub()
        tik_assets = assets_sub.tasks
        tik_shots = shots_sub.tasks
        tik_asset_names = set(tik_assets.keys())
        tik_shot_names = set(tik_shots.keys())

        # 3. Add new assets/shots from Tracktor
        for asset in tracktor_assets:
            if asset["asset_name"] not in tik_asset_names:
                self._sync_new_asset(asset, assets_sub, self.asset_categories)
        for shot in tracktor_shots:
            if shot["shot_name"] not in tik_shot_names:
                self._sync_new_shot(shot, shots_sub, self.shot_categories)

        # 4. Remove assets/shots from Tik that no longer exist in Tracktor
        for asset_name in tik_asset_names - tracktor_asset_names:
            assets_sub.remove_task(asset_name)
        for shot_name in tik_shot_names - tracktor_shot_names:
            shots_sub.remove_task(shot_name)

        # 5. (Optional) Update changed assets/shots
        # You can compare fields and update Tik if needed

        self.tik_main.project.settings.edit_property("last_sync", sync_stamp)
        self.tik_main.project.settings.apply_settings(force=True)

        return True, "Success"
    
    def sync_project(self):
        """
        Incrementally sync Tik Manager project with Tracktor project.
        Only pulls changes (add/update/delete) since the last sync.
        """
        sync_stamp = self.date_stamp()
        project_id = self.tik_main.project.settings.get("host_project_id")
        if not project_id:
            LOG.error("Project is not linked to a Tracktor project.")
            return False, "Project is not linked to a Tracktor project."

        management_platform = self.tik_main.project.settings.get("management_platform")
        if management_platform != "tracktor":
            LOG.error("Project is not linked to a Tracktor project.")
            return False, "Project is not linked to a Tracktor project."

        # 1. Get last sync time
        last_sync = self.tik_main.project.settings.get("last_sync")
        if not last_sync:
            # If never synced, do a full force_sync
            return self.force_sync(project_id)

        # 2. Fetch only changed assets/shots from Tracktor since last_sync
        # You need to implement these API endpoints in Tracktor!
        changed_assets = self.api.get_assets_since(project_id, last_sync)
        changed_shots = self.api.get_shots_since(project_id, last_sync)
        deleted_assets = self.api.get_deleted_assets_since(project_id, last_sync)
        deleted_shots = self.api.get_deleted_shots_since(project_id, last_sync)

        assets_sub = self._get_assets_sub()
        shots_sub = self._get_shots_sub()

        # 3. Add or update changed assets/shots
        for asset in changed_assets:
            self._sync_new_asset(asset, assets_sub, self.asset_categories)
        for shot in changed_shots:
            self._sync_new_shot(shot, shots_sub, self.shot_categories)

        # 4. Remove deleted assets/shots
        for asset_name in deleted_assets:
            assets_sub.remove_task(asset_name)
        for shot_name in deleted_shots:
            shots_sub.remove_task(shot_name)

        # 5. Update sync timestamp
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
        """Return the settings UI for the Tracktor platform."""
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

