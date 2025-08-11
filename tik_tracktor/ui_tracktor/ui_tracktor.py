"""UI Extension for Tracktor"""
from tik_manager4.ui.Qt import QtWidgets
from tik_manager4.ui.dialog.feedback import Feedback
from tik_manager4.management.ui.dialog import CreateFromManagementDialog
from tik_manager4.ui.widgets.pop import WaitDialog

from tik_manager4.management.extension_core import ExtensionCore
import sys
import os
sys.path.append(os.path.dirname(__file__))
from tracktor_api import TracktorAPI

import requests


class UiExtensions(ExtensionCore):
    def __init__(self, parent):
        print("UiExtensions __init__ called")
        self.parent = parent
        self.feedback = Feedback(parent=self.parent)

    def build_ui(self):
        """Build the extension UI."""
        print("build_ui called")
        self.add_main_menu()

    def add_main_menu(self):
        """Add the extension commands to the main menu."""
        print("add_main_menu called")
        tracktor_menu = self.parent.menu_bar.addMenu("Tracktor")

        login_action = QtWidgets.QAction("&Login", self.parent)
        tracktor_menu.addAction(login_action)
        login_action.triggered.connect(lambda: self.on_login())

        create_project_from_tracktor = QtWidgets.QAction("&Create Project from Tracktor", self.parent)
        tracktor_menu.addAction(create_project_from_tracktor)
        create_project_from_tracktor.triggered.connect(lambda: self.on_create_project_from_tracktor())

        force_sync = QtWidgets.QAction("&Force Sync", self.parent)
        tracktor_menu.addAction(force_sync)
        force_sync.triggered.connect(lambda: self.on_force_sync())

        tracktor_menu.addSeparator()
        logout_action = QtWidgets.QAction("&Logout", self.parent)
        tracktor_menu.addAction(logout_action)
        logout_action.triggered.connect(lambda: self.on_logout())

        check_connection_action = QtWidgets.QAction("&Check Tracktor Connection", self.parent)
        tracktor_menu.addAction(check_connection_action)
        check_connection_action.triggered.connect(lambda: self.on_check_connection())

    def on_check_connection(self):
        print("Tracktor connection button clicked!") 
        try:
            response = requests.get("http://localhost:8080/api/ping", timeout=5)
            response.raise_for_status()
            data = response.json()
            message = data.get("message", "No message in response")
        except Exception as e:
            message = f"Failed to connect: {e}"
        
        QtWidgets.QMessageBox.information(self.parent, "Tracktor Connection", message)


    def on_login(self):
        """
        Logs the user into its Tracktor environment
        """
        username, ok1 = QtWidgets.QInputDialog.getText(self.parent, "Login", "Username:")
        if not ok1 or not username:
            return
        password, ok2 = QtWidgets.QInputDialog.getText(self.parent, "Login", "Password:", QtWidgets.QLineEdit.Password)
        if not ok2 or not password:
            return

        self.api = TracktorAPI("http://localhost:8080/api", username, password)
        try:
            self.api.login()
            self.feedback.pop_info(title="Logged in", text="Logged into Tracktor")
        except Exception as e:
            self.feedback.pop_info(title="Error", text=f"Login failed: {e}")

    def on_create_project_from_tracktor(self):
        """
        Pulls the project from tracktor and hold connection for updates
        """
        if not hasattr(self, 'api') or not self.api:
            self.feedback.pop_info(title="Not logged in", text="Please login to Tracktor first.")
            return

        try:
            # 1. Get list of projects from Tracktor backend
            projects = self.api.get_projects()
            if not projects:
                self.feedback.pop_info(title="No projects", text="No projects found on Tracktor.")
                return

            # 2. Let the user pick one project
            project_names = [p['name'] for p in projects]
            selected, ok = QtWidgets.QInputDialog.getItem(
                self.parent, "Select Tracktor Project",
                "Choose a project:", project_names, 0, False
            )
            if not ok or not selected:
                return  # user cancelled

            # 3. Find the full project data
            project_data = next((p for p in projects if p['name'] == selected), None)
            if not project_data:
                self.feedback.pop_info(title="Not found", text="Selected project not found.")
                return

            # 4. Call TIK's CreateFromManagementDialog to create local project
            dialog = CreateFromManagementDialog(self.parent)#, project_data)
            dialog.exec_()

            # 5. Store the project ID for future syncing
            self.current_project_id = project_data['id']
            self.feedback.pop_info(title="Project created", text=f"Project '{selected}' created locally from Tracktor.")

        except Exception as e:
            self.feedback.pop_info(title="Error", text=f"Error creating project: {e}")

    def on_force_sync(self):
        """
        Overwrites the TIK project with Tracktor project data
        """

    def on_logout(self):
        """
        Logs out the user
        """

        # SIGNALS
        # login_action.triggered.connect(self.on_login)
        # create_project_from_tracktor.triggered.connect(
        #     self.on_create_project_from_tracktor
        # )
        # force_sync.triggered.connect(self.on_force_sync)
        # # for some reason, lambda is needed...
        # logout_action.triggered.connect(lambda: self.on_logout())