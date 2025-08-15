"""Credit to https://github.com/Colorbleed for the original code.
This is a modified version of the original code."""

import os
import logging
import re


from tik_manager4.ui.Qt import QtWidgets, QtGui, QtCore
from tik_manager4.ui import pick
from tik_manager4.external.tracktor.tracktor_api import TracktorAPI


LOG = logging.getLogger(__name__)
# set the log level to info
LOG.setLevel(logging.INFO)

class AnimatedLabel(QtWidgets.QLabel):
    """
    QLabel with animated background color.
    """

    def __init__(self):
        super(AnimatedLabel, self).__init__()
        self.setStyleSheet(
            """
            background-color: #CC4444;
            color: #F5F5F5;
            padding: 5px;
            """
        )
        self.setWordWrap(True)
        self.create_animation()

    def create_animation(self):
        """
        Create the animation of the color background.
        """
        color_begin = QtGui.QColor("#943434")
        color_end = QtGui.QColor("#CC4444")
        self.color_anim = QtCore.QPropertyAnimation(self, b"background_color")
        self.color_anim.setStartValue(color_begin)
        self.color_anim.setEndValue(color_end)
        self.color_anim.setDuration(400)

    def start_animation(self):
        """
        Start the animation of the color background.
        """
        self.color_anim.stop()
        self.color_anim.start()

    def get_back_color(self):
        """
        Get the background color.
        """
        return self.palette().color(QtGui.QPalette.Window)

    def set_back_color(self, color):
        """
        Set the given color as background color by parsing the style sheet.
        """
        style = self.styleSheet()
        pattern = "background-color:[^\n;]*"
        new = "background-color: %s" % color.name()
        style = re.sub(pattern, new, style, flags=re.MULTILINE)
        self.setStyleSheet(style)

    # Property to animate : the label background color
    background_color = QtCore.Property(
        QtGui.QColor, get_back_color, set_back_color
    )

class Login(QtWidgets.QDialog):
    """Log-in dialog to Tracktor"""

    logged_in = QtCore.Signal(bool)

    def __init__(self, api_class, parent=None, initialize_host=True):
        super(Login, self).__init__(parent)
        self.api_class = api_class
        self.api = None

        self.setWindowTitle("Connect to Tracktor")

        # style_file = pick.style_file()
        # self.setStyleSheet(str(style_file.readAll(), "utf-8"))

        # # Kitsu logo
        # logo_label = QtWidgets.QLabel()
        # pixmap = pick.pixmap("logo_kitsu.png")
        # logo_label.setPixmap(pixmap)
        # logo_label.setAlignment(QtCore.Qt.AlignCenter)

        form = QtWidgets.QFormLayout()
        form.setContentsMargins(10, 15, 10, 5)
        form.setObjectName("form")

        # Host
        host_label = QtWidgets.QLabel("Tracktor URL:")
        host_input = QtWidgets.QLineEdit()
        host_input.setPlaceholderText("https://localhost:8080/api")

        # User
        user_label = QtWidgets.QLabel("Username:")
        user_input = QtWidgets.QLineEdit()
        user_input.setPlaceholderText("jane-doe")

        # Password
        password_label = QtWidgets.QLabel("Password:")
        password_input = QtWidgets.QLineEdit()
        password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        # Error
        # error = AnimatedLabel()
        # error.hide()

        error = QtWidgets.QLabel()
        error.setStyleSheet("color: red;")
        error.hide()

        # Buttons
        login = QtWidgets.QPushButton("Login")
        login.setAutoDefault(True)
        login.setDefault(True)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(login)

        # Remember me
        remember_me_cb = QtWidgets.QCheckBox("Remember me")

        form.addRow(host_label, host_input)
        form.addRow(user_label, user_input)
        form.addRow(password_label, password_input)
        form.addRow(remember_me_cb)

        self.inputs = dict()
        self.inputs["host"] = host_input
        self.inputs["user"] = user_input
        self.inputs["password"] = password_input
        self.inputs["remember"] = remember_me_cb
        self.error = error

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(error)
        layout.addLayout(buttons)

        self.resize(325, 160)

        # Connections
        login.clicked.connect(self.on_login)

        if initialize_host:
            # Automatically enter host if available.
            self.initialize_host()

    def initialize_host(self):
        """Initialize host value based on environment"""
        host_input = self.inputs["host"]
        host = os.environ.get("TRACKTOR_HOST", None)
        if host:
            LOG.debug("Setting Tracktor host from environment variable TRACKTOR_HOST: %s" % host)
            host_input.setText(host)
            host_input.setEnabled(False)  # Optional: lock the field
        else:
            host_input.setText("http://localhost:8080/api")
            host_input.setEnabled(True)

    def on_login(self):
        """Perform login with current settings in the dialog."""

        host = self.inputs["host"].text()
        user = self.inputs["user"].text()
        password = self.inputs["password"].text()

        try:
            self.api = self.api_class(host, user, password)
            self.api.login()  # This should raise if login fails
        except Exception as exc:
            message = str(exc)
            self.error.setText(message)
            self.error.show()
            self.logged_in.emit(False)
            return

        self.logged_in.emit(True)
        self.accept()
