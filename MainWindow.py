
 # main window

from PySide6 import QtCore, QtWidgets, QtGui

from ProxyManager import ProxyManagerGUI
from ProfilesTable import ProfilesTable
from NewProfileForm import NewProfileForm
from Divider import Divider

from db import DatabaseConnection
import pandas as pd


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.load_csv_dialog = QtWidgets.QFileDialog(self, "Load Profiles from csv", filter="*.csv")
        self.setWindowTitle("Logger Bot")

        self.profile_table = ProfilesTable()
        self.add_profile_form = NewProfileForm()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.buttons_layout = QtWidgets.QHBoxLayout()

        self.proxy_manager = ProxyManagerGUI()
        self.manage_proxies_button = QtWidgets.QPushButton("Manage Proxies")

        self.add_profile_button = QtWidgets.QPushButton("Add Profile")

        self.load_from_csv_button = QtWidgets.QPushButton("Load Profiles from csv")


        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(Divider())
        self.layout.addWidget(self.profile_table)


        # set sizes
        self.manage_proxies_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.buttons_layout.addWidget(self.manage_proxies_button, alignment=QtCore.Qt.AlignLeft)
        self.buttons_layout.addWidget(self.add_profile_button, alignment=QtCore.Qt.AlignLeft)
        self.buttons_layout.addWidget(self.load_from_csv_button, alignment=QtCore.Qt.AlignLeft)
        self.setMinimumWidth(800)

    #        connection slots
        self.manage_proxies_button.clicked.connect(lambda : self.proxy_manager.show())
        self.add_profile_button.clicked.connect(lambda : self.add_profile_form.show())
        self.load_from_csv_button.clicked.connect(lambda : self.load_csv_dialog.show())
        self.load_csv_dialog.fileSelected.connect(self.on_load_csv)




    def on_load_csv(self, path: str):
        csv_path = path
        profile_data = pd.read_csv(csv_path)
        db_conn = DatabaseConnection("data/profiles.db").connection

        for index, row in profile_data.iterrows():
#             insert in sql
            sql_query = ("INSERT INTO profiles (profile_name,email,password, recovery_email,module_index, module_name,"
                         "proxy_ip, proxy_port, proxy_username, proxy_password)"
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            ip, port, username, password = row["proxy"].split(":")
            module_index = 0
            module_name = "Google"
            # random string for time being
            profile_name = "Profile " + str(index)
            db_conn.execute(sql_query, (profile_name, row["email"], row["password"], row["recovery_email"],
                                        module_index, module_name,
                                        ip, port, username, password))
            db_conn.commit()
        # self.profile_table.refresh_table()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # initialize the database
    db = DatabaseConnection("data/profiles.db")
    db.init_db()
    main_window = MainWindow()
    main_window.show()

    app.exec()