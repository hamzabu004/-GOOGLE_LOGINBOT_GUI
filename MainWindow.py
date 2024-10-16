import sys


from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from HeaderSection import HeaderSection
from ProfilesTable import ProfilesTable
from Divider import Divider

from db import DatabaseConnection
import pandas as pd

from globals import qt_styles
from utils import get_user_agent


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logger Bot")

        self.profile_table = ProfilesTable()
        self.profile_table.update_profile.set_main_window(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        self.header = HeaderSection(self.profile_table.refresh_table)
        self.header.setStyleSheet(qt_styles["btn"]["general"])
        self.layout.addWidget(self.header)
        self.layout.addWidget(Divider())
        self.layout.addWidget(self.profile_table)

        self.header.add_profile_form.set_main_window(self)
        # set sizes
        self.setMinimumWidth(800)

    #        connection slots


    def refresh_table(self):
        self.profile_table.refresh_table()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # initialize the database
    db = DatabaseConnection("data/profiles.db")
    db.init_db()
    main_window = MainWindow()
    main_window.show()

    app.exec()