from cProfile import label

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget


class FormInput(QtWidgets.QWidget):
    def __init__(self,  label: str):
        super().__init__()

        self.label = QtWidgets.QLabel(f"{label}:", self)
        self.label.setMinimumWidth(80)

        self.input = QtWidgets.QLineEdit(parent=self)


        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)

        self.input.textChanged.connect(self.print_text)

    def get_widget(self):
        return self

    def get_text(self):
        return self.input.text()

    @QtCore.Slot()
    def print_text(self):
        pass


class FormDropdown(QtWidgets.QWidget):
    def __init__(self, label: str, items: list):
        super().__init__()

        self.selected_item_index = 0

        self.label = QtWidgets.QLabel(f"{label}:", self)
        self.label.setMinimumWidth(80)

        self.dropdown = QtWidgets.QComboBox(self)
        self.dropdown.addItems(items)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)


    def get_widget(self):
        return self

    def get_selected_index(self):
        return self.dropdown.currentIndex()

    def get_text(self):
        return self.dropdown.currentText()