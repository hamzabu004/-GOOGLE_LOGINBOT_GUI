from PySide6 import QtWidgets, QtCore
from numpy.f2py.symbolic import as_eq

from CaptchaManager import CaptchaManager
from NewProfileForm import NewProfileForm
from utils import on_load_csv, get_user_agent
from globals import  qt_styles


class HeaderSection (QtWidgets.QWidget) :
    def __init__(self, refresh_table):
        super().__init__()
        self.load_csv_dialog = QtWidgets.QFileDialog(self, "Load Profiles from csv", filter="*.csv")

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(2)

        self.captcha_manager = CaptchaManager()
        self.add_profile_form = NewProfileForm()
        self.add_profile_button = QtWidgets.QPushButton("Add Profile")
        self.load_from_csv_button = QtWidgets.QPushButton("Load Profiles from csv")
        self.change_api_button = QtWidgets.QPushButton("2Captcha Key")

        self.layout.addWidget(self.add_profile_button, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.load_from_csv_button, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.change_api_button, alignment=QtCore.Qt.AlignLeft)

        self.add_profile_button.clicked.connect(self.launch_profile_form)
        self.load_from_csv_button.clicked.connect(lambda : self.load_csv_dialog.show())
        self.load_csv_dialog.fileSelected.connect(lambda path: on_load_csv(path, refresh_table))
        self.change_api_button.clicked.connect(self.launch_captcha_manager)


    def launch_profile_form(self):
        self.add_profile_form.set_user_agent(get_user_agent())
        self.add_profile_form.show()

    def launch_captcha_manager(self):
        self.captcha_manager.set_key()
        self.captcha_manager.show()


#         customize button
