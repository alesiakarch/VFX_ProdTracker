"""UI Extension for Tracktor"""
from tik_manager4.ui.Qt import QtWidgets
from tik_manager4.ui.dialog.feedback import Feedback
from tik_manager4.management.ui.dialog import CreateFromManagementDialog
from tik_manager4.ui.widgets.pop import WaitDialog

from tik_manager4.management.extension_core import ExtensionCore

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

        create_project_from_tracktor = QtWidgets.QAction("&Create Project from Tracktor", self.parent)
        tracktor_menu.addAction(create_project_from_tracktor)

        force_sync = QtWidgets.QAction("&Force Sync", self.parent)
        tracktor_menu.addAction(force_sync)

        tracktor_menu.addSeparator()
        logout_action = QtWidgets.QAction("&Logout", self.parent)
        tracktor_menu.addAction(logout_action)

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
        # SIGNALS
        # login_action.triggered.connect(self.on_login)
        # create_project_from_tracktor.triggered.connect(
        #     self.on_create_project_from_tracktor
        # )
        # force_sync.triggered.connect(self.on_force_sync)
        # # for some reason, lambda is needed...
        # logout_action.triggered.connect(lambda: self.on_logout())