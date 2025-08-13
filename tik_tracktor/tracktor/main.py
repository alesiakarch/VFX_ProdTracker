"""Main module for Tracktor integration."""
from tik_manager4.management.management_core import ManagementCore
from tik_manager4.core.constants import DataTypes 
from tik_manager4.external.tracktor.tracktor_api import TracktorAPI
from tik_manager4.management.tracktor.ui.login import Login

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

    def create_from_project(self):
        """This method is called when a new project is created."""
        raise NotImplementedError("The method 'create_project' must be implemented.")

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

