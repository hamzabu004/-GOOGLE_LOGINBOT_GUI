import copy

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFrame

from Divider import Divider
from gui_utils import FormInput

from WebsiteForm import WebsiteForm


class NewProfileForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.profile_name = FormInput("Profile Name")
        self.website = WebsiteForm()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        self.layout.addWidget(self.profile_name)

        self.layout.addWidget(Divider())
        self.layout.addWidget(self.website)

    def get_profile_data(self):
        return {
            "profile_name": self.profile_name.get_text(),
            "proxy": self.proxy.get_proxy_data(),
            "website": self.website.get_website_data()
        }