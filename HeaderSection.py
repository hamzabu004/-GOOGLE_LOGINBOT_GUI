from PySide6 import QtWidgets, QtCore

from NewProfileForm import NewProfileForm
from utils import on_load_csv
from globals import  qt_styles


class HeaderSection (QtWidgets.QWidget) :
    def __init__(self, refresh_table):
        super().__init__()
        self.load_csv_dialog = QtWidgets.QFileDialog(self, "Load Profiles from csv", filter="*.csv")

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(2)

        self.add_profile_form = NewProfileForm()
        self.add_profile_button = QtWidgets.QPushButton("Add Profile")
        self.load_from_csv_button = QtWidgets.QPushButton("Load Profiles from csv")

        self.layout.addWidget(self.add_profile_button, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.load_from_csv_button, alignment=QtCore.Qt.AlignLeft)

        self.add_profile_button.clicked.connect(lambda : self.add_profile_form.show())
        self.load_from_csv_button.clicked.connect(lambda : self.load_csv_dialog.show())
        self.load_csv_dialog.fileSelected.connect(lambda path: on_load_csv(path, refresh_table))





#         customize button
