from PySide6 import QtWidgets
from gui_utils import FormInput, FormDropdown

class WebsiteForm(QtWidgets.QWidget):
    available_websites = ["google", "facebook", "twitter", "instagram"]
    def __init__(self):
        super().__init__()


        self.url = FormDropdown("URL", self.available_websites)
        self.proxy = FormDropdown("Proxy", ["proxy1", "proxy2", "proxy3"])
        self.user = FormInput("Email")
        self.password = FormInput("Password")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        self.layout.addWidget(self.url)
        self.layout.addWidget(self.proxy)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.password)

    def get_website_data(self):
        return {
            "url": self.url.get_text(),
            "user": self.user.get_text(),
            "password": self.password.get_text()
        }