import json

import PySide6.QtWidgets as QWidgets

from gui_utils import FormInput


class CaptchaManager(QWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        self.api_key = FormInput("2Captcha API Key")
        self.layout.addWidget(self.api_key)

        self.save_button = QWidgets.QPushButton("Save", self)
        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.on_save)

    def set_key(self):
        try:
            with open("data/config.json", "r") as f:
                config = json.load(f)
            if "2CAPTCHA_API_KEY" in config:
                self.api_key.set_text(config["2CAPTCHA_API_KEY"])

        except FileNotFoundError as e:
            self.api_key.set_text("")


    def on_save(self):
        config = dict()
        try:
            with open("data/config.json", "r") as f:
                config = json.load(f)
                config["2CAPTCHA_API_KEY"] = self.api_key.get_text()
        except FileNotFoundError as e:
            config["2CAPTCHA_API_KEY"] = self.api_key.get_text()

        with open("data/config.json", "w") as f:
            json.dump(config, f)

        self.close()
