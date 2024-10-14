import re
from PySide6 import QtWidgets
from pyexpat.errors import messages
import uuid
from Divider import Divider
from gui_utils import FormInput, FormDropdown
from db import DatabaseConnection

class Proxy:
    schemes = ["http", "https"]
    def __init__(self, id, name: str, ip: str, port: int,
                 is_public = False, username = None, password = None,
                 scheme_idx = 0):

        self.id = id
        self.proxy_name = name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.is_public = is_public

        self.scheme_index = scheme_idx

    def __str__(self):
        return f"{self.ip}:{self.port}"

class ProxyManager:
    def __init__(self):
        self.proxies = []

    def add_proxy(self, proxy):
        conn = DatabaseConnection("data/bot.db").connection
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO proxies (id, proxy_name, scheme ip, port, username, password) "
                       f"VALUES ('{proxy.id}, {proxy.proxy_name}', {proxy.schemes[0]},  '{proxy.ip}', '{proxy.port}', "
                       f"'{proxy.username}', '{proxy.password}')")
        pass

    def update_proxy(self, proxy):
        #update proxy in database
        pass

    def delete_proxy(self, proxy):
        #delete proxy from database
        pass

    def update_proxy_list(self):
        #update proxy list from database
        pass

    def get_proxy(self):
        db = DatabaseConnection("data/bot.db")
        conn = db.connection
        cursor = conn.cursor()

        cursor.execute("SELECT id, proxy_name, ip, port, username, password FROM proxies")

        for row in cursor.fetchall():
            proxy = Proxy(id=row[0], name=row[1], ip=row[2], port=row[3], username=row[4], password=row[5])
            self.proxies.append(proxy)

# interface for proxy manager

class ProxyManagerGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # it will work with database
        self.proxy_manager = ProxyManager()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.add_proxy_button = QtWidgets.QPushButton("Add Proxy")
        self.add_proxy_button.clicked.connect(self.add_proxy)

        self.test_proxies_button = QtWidgets.QPushButton("Test Proxies")
        self.test_proxies_button.clicked.connect(self.test_proxies)

        self.menu_buttons_layout = QtWidgets.QHBoxLayout()
        self.menu_buttons_layout.setSpacing(2)
        self.menu_buttons_layout.addWidget(self.add_proxy_button)
        self.menu_buttons_layout.addWidget(self.test_proxies_button)

        self.layout.addLayout(self.menu_buttons_layout)
        self.layout.addWidget(Divider())

        self.add_proxy_dialog =  None

        # table for proxies
        self.proxies_table = ProxyTable(proxies=self.proxy_manager.proxies)
        self.layout.addWidget(self.proxies_table)
        # self.layout.addWidget(self.add_proxy_button)
        self.layout.addWidget(self.proxies_table)

    #     set size
        self.setMinimumSize(600, 400)

    def add_proxy(self):
        self.add_proxy_dialog = AddProxyDialog(proxy_manager=self.proxy_manager)
        self.add_proxy_dialog.show()

    def test_proxies(self):
        pass

    def get_proxy_manager(self):
        return self.proxy_manager

    def get_widget(self):
        return self

    def update_proxy_table(self):
        self.proxies_table.clear()
        for proxy in self.proxy_manager.proxies:
            self.proxies_table.add_proxy(proxy)

class AddProxyDialog(QtWidgets.QWidget):
    def __init__(self, proxy: Proxy = None, proxy_manager: ProxyManager = None):
        super().__init__()

        self.proxy_manager = proxy_manager
        self.proxy = proxy

        self.setWindowTitle("Add/Edit Proxy")

        self.name = FormInput("Title")
        self.server = FormInput("Server")
        self.port = FormInput("Port")
        self.public_port = QtWidgets.QCheckBox("Public Port")
        self.proxy_type = FormDropdown("Proxy Type", Proxy.schemes)

        self.isOpenProxy = False

        self.user = FormInput("User")
        self.password = FormInput("Password")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(2)

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.server)
        self.layout.addWidget(self.port)
        self.layout.addWidget(self.proxy_type)
        self.layout.addWidget(self.public_port)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.password)

        self.setLayout(self.layout)
        self.save_button = QtWidgets.QPushButton('Save' if not proxy else 'Update')

        self.cancel_button = QtWidgets.QPushButton('Cancel')

        self.buttons_layout = QtWidgets.QHBoxLayout(self)
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)

        # connecting slots
        self.public_port.stateChanged.connect(self.toggle_account_input)
        self.save_button.clicked.connect(self.save_proxy)
        self.cancel_button.clicked.connect(self.close)

    def toggle_account_input(self):
        if self.public_port.isChecked():
            self.user.input.setDisabled(True)
            self.password.input.setDisabled(True)
        else:
            self.user.input.setDisabled(False)
            self.password.input.setDisabled(False)

    def save_proxy(self):
        success_flag = False
        validate_message = self.validate_form()

        if self.validate_form() != "True":
            return

        print("Saving Proxy")
        #  adding new proxy
        if not self.proxy:
            self.proxy = Proxy(self.server.get_text(), self.port.get_text(), self.user.get_text(), self.password.get_text())
            if self.proxy_manager.add_proxy(self.proxy):
                print("Proxy Added")
                success_flag = True

        else :
            if self.proxy_manager.update_proxy(self.proxy):
                print("Proxy Updated")
                success_flag = True
        if success_flag:
            self.close()
        else:
            # show error dialog
            pass


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

class ProxyTable(QtWidgets.QWidget):
    def __init__(self, proxies):
        super().__init__()
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type" "Server", "Port", "User", "Working"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.table)
        for proxy in proxies:
            self.add_proxy(proxy)

    def add_proxy(self, proxy):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(proxy.id)))

    def update_proxy_status(self, index: int, status: bool):
        self.table.setItem(index, 5, QtWidgets.QTableWidgetItem("Yes" if status else "No"))


