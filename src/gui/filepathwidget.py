#! /usr/env python
# gui/filepathwidget.py : widget for picking input files 

# QT
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QSizePolicy)
from PySide6.QtCore import Qt


class FilePathWidget(QWidget) :
    def __init__(self, parent = None) :
        super(FilePathWidget, self).__init__(parent)
        # subwidgets
        self.textbox = QLineEdit()
        self.selectbtn = QPushButton("pick")
        self.selectbtn.clicked.connect(self.on_button_clicked)
        
        # layout
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.textbox)
        horizontalLayout.addWidget(self.selectbtn)
        horizontalLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setLayout(horizontalLayout)
        
        # size policy
        self.textbox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

    def on_button_clicked(self, event):
        filepath, _filter = QFileDialog.getOpenFileName(self, 'Select Path')
        self.textbox.setText(filepath)

    def path(self) -> str :
        return self.textbox.text()
        
