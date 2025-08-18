import requests

class TracktorAPI:
    """
    Tracktor API wrapper for Tracktor integration into TIK Manager.
    Sends requests for Tracktor backend directly. 

    Attributes:
        base_url (str): The base URL of the Tracktor backend.
        username (str): Username for authentication.
        password (str): Password for authentication.

    """


    def __init__(self, base_url, username=None, password=None):
        """
        Initializes the TracktorAPI instance.

        Args:
            base_url (str): The base URL of the Tracktor backend.
            username (str, optional): Username for authentication.
            password (str, optional): Password for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password

    def api_request(self, method, endpoint, **kwargs):
        """
        Sends an HTTP request to the Tracktor backend.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST', 'PUT').
            endpoint (str): API endpoint (e.g., '/projects').
            **kwargs: Additional arguments.

        Returns:
            dict or None: The JSON response from the backend, or None if no content.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
                
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})

        if self.username and self.password:
            headers["X-Username"] = self.username
            headers["X-Password"] = self.password

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return None

    def login(self):
        """
        Checks that the usename and password are present before passing them to authentication

        Returns:
            bool: True if credentials are present.

        Raises:
            ValueError: If username or password is missing.
        """

        if not self.username or not self.password:
            raise ValueError("Username and password required")
        
        credentials = {
            "user_name" : self.username,
            "user_password" : self.password
        }

        response = self.api_request("POST", "/login", json=credentials)
        if response and response.get("success"):
            return True
        else:
            return False

    def logout(self):
        """
        Logs out the current user by clearing credentials.

        Returns:
            bool: True if logout was successful.
        """
        self.username = None
        self.password = None
        return True

    def get_project(self, project_id):
        """
        Retrieves a project by its ID.

        Args:
            project_id (int): The project id.

        Returns:
            dict: Project data.
        """
        return self.api_request("GET", f"/projects/{project_id}")
    
    def get_projects(self):
        """
        Retrieves all projects.

        Returns:
            list: A list of project data dictionaries.
        """
        return self.api_request("GET", f"/projects")

    def get_shots(self, project_id):
        """
        Retrieves all shots for a given project.

        Args:
            project_id (int): The project id.

        Returns:
            list: A list of shot data dictionaries.
        """
        return self.api_request("GET", f"/projects/{project_id}/shots")

    def get_assets(self, project_id):
        """
        Retrieves all assets for a given project.

        Args:
            project_id (int): The project id.

        Returns:
            list: A list of asset data dictionaries.
        """
        return self.api_request("GET", f"/projects/{project_id}/assets")
