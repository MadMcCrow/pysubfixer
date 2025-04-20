#! /usr/env python
# gui/mainwidget.py : main application window

from typing import Callable
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout
from filepathwidget import FilePathWidget
from numericwidget import NumericWidget

class MainWidget(QMainWindow) :
    def __init__(self, runcmd : Callable, name="pysubfixer-gui") :
        super(MainWidget, self).__init__()
        self.runcmd = runcmd
        self.resize(500, 250)
        self.setWindowTitle(name)
       
        # our path widgets
        self.videoWidget = FilePathWidget("Video")
        self.subtitleWidget = FilePathWidget("Subtitle")
        self.delayWidget = NumericWidget()

        # execute button
        self.runbutton = QPushButton("Execute")
        self.runbutton.clicked.connect(self.onExec)

        # a nice simple layout
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.videoWidget)
        verticalLayout.addWidget(self.subtitleWidget)
        verticalLayout.addWidget(self.delayWidget)
        verticalLayout.addWidget(self.runbutton)
        widget = QWidget()
        widget.setLayout(verticalLayout)
        self.setCentralWidget(widget)
    
    def onExec(self) :
        command = {
            "source": self.videoWidget.get_path(),
            "subs"  : self.subtitleWidget.get_path(),
            "delay" : self.delayWidget.get_time()
        }
        self.runcmd(command)

