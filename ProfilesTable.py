import os

from shutil import rmtree
from PySide6 import QtWidgets

from NewProfileForm import NewProfileForm
from ProfilesManager import ProfilesManager
from db import DatabaseConnection
from globals import qt_styles
from utils import delete_from_db, rm_dir


class ProfilesTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.profiles = []
        self.update_profile = NewProfileForm()

        self.profile_manager = ProfilesManager()
        # laod from db
        conn = DatabaseConnection("data/profiles.db").connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles")
        profiles = cursor.fetchall()
        self.columns = ["Profile Name", "Proxy", "Email", "Module"]
        self.setColumnCount(len(self.columns) + 1)
        self.setHorizontalHeaderLabels(self.columns)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for profile in profiles:
            self.insert_profile(profile)


    def insert_profile(self, profile):

        self.insertRow(len(self.profiles))
        self.setItem(len(self.profiles), 0, QtWidgets.QTableWidgetItem(profile["profile_name"]))
        self.setItem(len(self.profiles), 1, QtWidgets.QTableWidgetItem(profile["proxy_ip"]))
        self.setItem(len(self.profiles), 2, QtWidgets.QTableWidgetItem(profile["email"]))
        self.setItem(len(self.profiles), 3, QtWidgets.QTableWidgetItem(profile["module_name"]))

        launch_button = QtWidgets.QPushButton("Launch")
        launch_button.setStyleSheet(qt_styles["btn"]["green"])

        edit_button = QtWidgets.QPushButton("Edit")

        delete_button = QtWidgets.QPushButton("Delete")

        actions = QtWidgets.QWidget()
        actions_layout = QtWidgets.QVBoxLayout(actions)
        actions_layout.addWidget(launch_button)
        actions_layout.addWidget(edit_button)
        actions_layout.addWidget(delete_button)

        self.setCellWidget(len(self.profiles), 4, actions)
        self.resizeRowToContents(len(self.profiles))
        self.resizeColumnsToContents()

         # slots
        launch_button.clicked.connect(lambda : self.launch_profile(profile))
        edit_button.clicked.connect(lambda : self.edit_profile(profile))
        delete_button.clicked.connect(lambda : self.delete_profile(profile["id"]))
        self.profiles.append(profile)

    def launch_profile(self, profile):
        self.profile_manager.launch_profile(profile)

    def edit_profile(self, profile):

        self.update_profile.set_update(profile)
        self.update_profile.show()

    def delete_profile(self, id):
        delete_from_db("DELETE FROM profiles WHERE id = ?", (id,))
        #     check profile directory
        path = os.getcwd() + "\\data\\profiles\\" + str(id)
        rm_dir(path)
        self.refresh_table()

    def refresh_table(self):
        print("refreshing table...")
        self.clear()
        self.profiles = []
        conn = DatabaseConnection("data/profiles.db").connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles")
        profiles = cursor.fetchall()
        print()
        for profile in profiles:
            self.insert_profile(profile)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
