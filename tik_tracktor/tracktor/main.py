"""Main module for Tracktor integration."""
from .tracktor_api import TracktorAPI
from tik_manager4.management.management_core import ManagementCore
from tik_manager4.core.constants import DataTypes 
from .ui_tracktor import UiExtensions

# add external folder with extra dependancies if needed
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
        self.is_authenticated = False # user isnt logged in yet
        self.user = None # no user data at the init

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
        url = self.host_api
        username = getattr(self, "tracktor_username", None)
        password = getattr(self, "tracktor_password", None)
        
        if not url or not username or not password:
            self.api = None
            self.is_authenticated = False
            self.user = None
            return None, "Missing Tracktor URL, username, or password in settings."
        
        self.api = TracktorAPI(url, username, password)

        try:
            self.api.login()
            self.is_authenticated = True
            self.user = username
            return self.api, "Authenticated"
        
        except Exception as e:
            self.api = None
            self.is_authenticated = False
            self.user = None
            return None, f"Authentication failed: {e}"
        
    def logout(self):
        """Logout the user."""
        if self.api:
            try:
                self.api.logout()
            except Exception as e:
                print(f"Tracktor logout failed: {e}")
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

    @staticmethod # sets settings 
    def get_settings_ui():
        """Return the settings UI for the Tracktor platform."""
        # Make sure the keys are unique accross all other platforms
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

