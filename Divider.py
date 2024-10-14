from PySide6 import QtWidgets

class Divider(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QtWidgets.QFrame.HLine)  # Horizontal line
        self.setFrameShadow(QtWidgets.QFrame.Sunken)