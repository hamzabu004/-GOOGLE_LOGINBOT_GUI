from PySide6 import QtWidgets
from gui_utils import FormInput, FormDropdown

class WebsiteForm(QtWidgets.QWidget):
    available_websites = ["google", "facebook", "twitter", "instagram"]
    def __init__(self):
        super().__init__()

        self.url = FormDropdown("URL", self.available_websites)
        self.user = FormInput("Email")
        self.password = FormInput("Password")
        self.recover_email = FormInput("Recovery Email")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.url)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.recover_email)

    def set_website_data(self, profile):
        self.url.set_option(self.available_websites.index((profile["module_name"]).lower()))
        self.user.set_text(profile["email"])
        self.password.set_text(profile["password"])
        self.recover_email.set_text(profile["recovery_email"])

    def get_website_data(self):
        return {
            "module_name": self.url.get_text(),
            "module_index": self.url.get_text(),
            "email": self.user.get_text(),
            "password": self.password.get_text(),
            "recovery_email": self.recover_email.get_text()
        }

    def clear(self):
        self.url.set_option(0)
        self.user.set_text("")
        self.password.set_text("")
        self.recover_email.set_text("")