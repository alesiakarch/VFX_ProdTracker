"""UI Extension for Tracktor"""
from tik_manager4.ui.Qt import QtWidgets
from tik_manager4.ui.dialog.feedback import Feedback
from tik_manager4.management.ui.dialog import CreateFromManagementDialog
from tik_manager4.ui.widgets.pop import WaitDialog

from tik_manager4.management.extension_core import ExtensionCore

class UiExtensions(ExtensionCore):
    def __init__(self, parent):
        self.parent = parent
        self.feedback = Feedback(parent=self.parent)

    def build_ui(self):
        """Build the extension UI."""
        self.add_main_menu()

    def add_main_menu(self):
        """Add the extension commands to the main menu."""
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

        # SIGNALS
        # login_action.triggered.connect(self.on_login)
        # create_project_from_tracktor.triggered.connect(
        #     self.on_create_project_from_tracktor
        # )
        # force_sync.triggered.connect(self.on_force_sync)
        # # for some reason, lambda is needed...
        # logout_action.triggered.connect(lambda: self.on_logout())