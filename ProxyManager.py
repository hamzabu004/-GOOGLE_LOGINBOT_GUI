import re
from PySide6 import QtWidgets, QtCore

import globals
from gui_utils import FormInput, FormDropdown


class Proxy:

    def __init__(self, ip: str, port: int,
                 is_public = False, username = None, password = None,
                 scheme_idx = 0):

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.is_public = is_public

        self.scheme_index = scheme_idx

    def __str__(self):
        return f"{self.ip}:{self.port}"


class ProxyForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()



        self.server = FormInput("Server")
        self.port = FormInput("Port")
        self.public_port = QtWidgets.QCheckBox("Public Port")
        self.proxy_type = FormDropdown("Proxy Type", globals.proxy_schemes)

        self.isOpenProxy = False

        self.user = FormInput("User")
        self.password = FormInput("Password")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        self.layout.addWidget(self.server)
        self.layout.addWidget(self.port)
        self.layout.addWidget(self.proxy_type)
        self.layout.addWidget(self.public_port)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.password)



        # connecting slots
        self.public_port.stateChanged.connect(self.toggle_account_input)

    def toggle_account_input(self):
        if self.public_port.isChecked():
            self.user.input.setDisabled(True)
            self.password.input.setDisabled(True)
        else:
            self.user.input.setDisabled(False)
            self.password.input.setDisabled(False)


    def validate_form(self) -> bool:
        # check for empty fields
        if (not self.server.get_text() or not self.port.get_text() or
                (not self.public_port.isChecked() and (not self.user.get_text() or not self.password.get_text()))):
            print("Empty Text")
            return False

        # check for valid port and ip
        elif not self.port.get_text().isdigit():
            return False
        ip_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if not re.fullmatch(ip_regex, self.server.get_text()):
            return False

        return True

    def get_proxy_data(self):
        return {
            "proxy_ip": self.server.get_text(),
            "proxy_port": self.port.get_text(),
            "proxy_type": self.proxy_type.get_text(),
            "proxy_username": self.user.get_text(),
            "proxy_password": self.password.get_text(),

        }

    def set_proxy_data(self, profile):
        self.server.set_text(profile["proxy_ip"])
        self.port.set_text(profile["proxy_port"])
        self.proxy_type.set_option(globals.proxy_schemes.index(profile["proxy_type"]))
        self.user.set_text(profile["proxy_username"])
        self.password.set_text(profile["proxy_password"])

    def clear(self):
        self.server.set_text("")
        self.port.set_text("")
        self.proxy_type.set_option(0)
        self.user.set_text("")
        self.password.set_text("")