import requests

class TracktorAPI:

    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.token = None  # For future token auth

    def api_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        elif self.username and self.password:
            headers["X-Username"] = self.username
            headers["X-Password"] = self.password

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return None

    def login(self):
        # Currently just verifies username/password presence
        # In future, exchange creds for token here
        if not self.username or not self.password:
            raise ValueError("Username and password required")
        # Optionally test connection or credentials here
        return True

    def logout(self):
        self.token = None
        self.username = None
        self.password = None
        return True

    def get_project(self, project_id):
        return self.api_request("GET", f"/projects/{project_id}")
    
    def get_projects(self):
        return self.api_request("GET", f"/projects")

    def get_shots(self, project_id):
        return self.api_request("GET", f"/projects/{project_id}/shots")

    def get_assets(self, project_id):
        return self.api_request("GET", f"/projects/{project_id}/assets")

    def update_shot_status(self, shot_id, status):
        data = {"status": status}
        return self.api_request("PUT", f"/shots/{shot_id}", json=data)