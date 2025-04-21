#! /usr/env python
# gui/numericwidget.py : widget for selecting numbers

from PySide6.QtWidgets import QSpinBox, QSizePolicy
from sys import maxsize

class NumericWidget(QSpinBox) :
    """
    A widget that allows selecting integers
    """
    def __init__(self, parent = None) :
        super(NumericWidget, self).__init__(parent)
        self.setValue(0)
        # max possible range
        self.setRange(-2147483648,2147483647)
        # create layout
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    