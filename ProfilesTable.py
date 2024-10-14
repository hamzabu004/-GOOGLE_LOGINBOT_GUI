from PySide6 import QtWidgets, QtGui

from ProfilesManager import ProfilesManager
from db import DatabaseConnection


class ProfilesTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.profiles = []
        self.profile_manager = ProfilesManager()
        # laod from db
        conn = DatabaseConnection("data/profiles.db").connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles")
        profiles = cursor.fetchall()
        self.columns = ["Profile Name", "Proxy", "Email", "Module"]
        self.setColumnCount(len(self.columns) + 1)
        self.setHorizontalHeaderLabels(self.columns)
        for profile in profiles:
            self.insert_profile(profile)


    def insert_profile(self, profile):

        self.insertRow(len(self.profiles))
        self.setItem(len(self.profiles), 0, QtWidgets.QTableWidgetItem(profile["profile_name"]))
        self.setItem(len(self.profiles), 1, QtWidgets.QTableWidgetItem(profile["proxy_ip"]))
        self.setItem(len(self.profiles), 2, QtWidgets.QTableWidgetItem(profile["email"]))
        self.setItem(len(self.profiles), 3, QtWidgets.QTableWidgetItem(profile["module_name"]))

        launch_button = QtWidgets.QPushButton("Launch")
        launch_button.setStyleSheet("background-color: green")

        edit_button = QtWidgets.QPushButton("Edit")

        actions = QtWidgets.QWidget()
        actions_layout = QtWidgets.QVBoxLayout(actions)
        actions_layout.addWidget(launch_button)
        actions_layout.addWidget(edit_button)

        self.setCellWidget(len(self.profiles), 4, actions)
        self.resizeRowToContents(len(self.profiles))
        self.resizeColumnsToContents()

         # slots
        launch_button.clicked.connect(lambda : self.launch_profile(profile))
        edit_button.clicked.connect(lambda : self.edit_profile(profile))
        self.profiles.append(profile)

    def launch_profile(self, profile):
        self.profile_manager.launch_profile(profile)

    def edit_profile(self, profile):
        pass
