
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFrame

import globals
import utils
from Divider import Divider
from ProxyManager import ProxyForm
from gui_utils import FormInput, FormDropdown
from globals import proxy_schemes
from WebsiteForm import WebsiteForm
from utils import insert_to_db


class NewProfileForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.is_update = False
        self.profile_name = FormInput("Profile Name")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.profile_name)
        self.layout.addWidget(Divider())

        self.combined_layout = QtWidgets.QHBoxLayout(self)

        self.website = WebsiteForm()

        self.profile_layout = QtWidgets.QVBoxLayout(self)
        self.profile_layout.setSpacing(2)

        self.user_agent = FormInput("User Agent")


        self.profile_layout.addWidget(self.website)
        self.profile_layout.addWidget(self.user_agent)

        self.combined_layout.addLayout(self.profile_layout)

        self.proxy_form = ProxyForm()
        self.combined_layout.addWidget(self.proxy_form)

        self.layout.addLayout(self.combined_layout)

        self.button_layout = QtWidgets.QHBoxLayout(self)
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)


        self.button_layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)

        self.layout.addWidget(Divider())
        self.layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.on_save_profile)
        self.cancel_button.clicked.connect(self.on_cancel)

    def set_main_window(self, main_window):
        self.main_window = main_window

    def get_profile(self):
        profile = {"profile_name": self.profile_name.get_text(), "user_agent": self.user_agent.get_text()}
        profile.update(self.website.get_website_data())
        profile.update(self.proxy_form.get_proxy_data())

        return profile



    def on_save_profile(self):
        profile = self.get_profile()
        params = utils.get_params_profile_read(profile)
        print(params)
        insert_to_db(globals.sql_queries["insert_profile"], params, self.main_window.refresh_table)
        self.on_cancel()

    def on_update_profile(self):
        pass

    def on_cancel(self):
        self.clear()
        self.close()


    def clear(self):
        self.profile_name.set_text("")
        self.website.clear()
        self.proxy_form.clear()
        self.user_agent.set_text("")

    def set_update(self):
        self.is_update = True
        self.save_button.setText("Update")
        self.save_button.clicked.connect(self.on_update_profile)

    def clear_update(self):
        self.is_update = False
        self.save_button.setText("Save")
        self.clear()
        self.save_button.clicked.connect(self.on_save_profile)


