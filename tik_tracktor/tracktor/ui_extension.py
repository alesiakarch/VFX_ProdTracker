"""UI Extension for Tracktor"""
from tik_manager4.ui.Qt import QtWidgets
from tik_manager4.ui.dialog.feedback import Feedback
from tik_manager4.management.ui.dialog import CreateFromManagementDialog
from tik_manager4.ui.widgets.pop import WaitDialog

from tik_manager4.management.extension_core import ExtensionCore

# path to the tracktor plugin
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

        try:
            print("Available management handlers:", getattr(self.parent, "management_handlers", None))
            handler = self.parent.management_connect("tracktor")
            if handler:
                handler.tracktor_username = username
                handler.tracktor_password = password
                if not handler.is_authenticated:
                    self.feedback.pop_info(title="Error", text="Login failed: Invalid credentials or missing URL.")
                    return
            self.feedback.pop_info(title="Logged in", text="Logged into Tracktor")
        
        except Exception as e:  
            self.feedback.pop_info(title="Error", text=f"Login failed: {e}")

    def on_create_project_from_tracktor(self):
        """
        Pulls the project from tracktor and hold connection for updates
        """
        print("Create Project from Tracktor clicked")
        if not self.parent._pre_check(level=3):
            print("Pre-check failed")
            return
        print("Available management handlers:", getattr(self.parent, "management_handlers", None))
        handler = self.parent.management_connect("tracktor")
        if not handler:
            print("Handler missing")
            return
        
        print("Opening dialog")
        dialog = CreateFromManagementDialog(handler, parent=self.parent)
        state = dialog.exec()

        print("Dialog closed, state:", state)
        if state:
            self.parent.refresh_project()
            self.parent.status_bar.showMessage("Project created successfully")

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