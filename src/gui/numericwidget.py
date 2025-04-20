#! /usr/env python
# gui/numericwidget.py : widget for selecting numbers

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel

class NumericWidget(QWidget) :
    """
    A widget that allows selecting integers
    """
    def __init__(self, parent = None) :
        super(NumericWidget, self).__init__(parent)
        self.textbox = QLineEdit("0")
        # TODO : support validators
        #self.textbox.setValidator(Qt.QIntValidator())
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(QLabel("Delay :"))
        horizontalLayout.addWidget(self.textbox)
        self.setLayout(horizontalLayout)

    def get_value(self) -> int :
        #TODO : handle errors !
        return int(self.textbox.text())
