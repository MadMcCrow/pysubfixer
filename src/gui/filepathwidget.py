#! /usr/env python
# gui/filepathwidget.py : widget for picking input files 

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel

class FilePathWidget(QWidget) :
    def __init__(self, name : str, parent = None) :
        super(FilePathWidget, self).__init__(parent)
        self.textbox = QLineEdit()
        self.selectbtn = QPushButton("pick")
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(QLabel(f"{name}:"))
        horizontalLayout.addWidget(self.textbox)
        horizontalLayout.addWidget(self.selectbtn)
        self.setLayout(horizontalLayout)
        self.selectbtn.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self, event):
        filepath, _filter = QFileDialog.getOpenFileName(self, 'Select Path')
        self.textbox.setText(filepath)

    def get_path(self) -> str :
        return self.textbox.text()
        
