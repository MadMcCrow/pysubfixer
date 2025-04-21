#! /usr/env python
# gui/mainwidget.py : main application window

# python
from sys import argv
from typing import Callable

# PySide6
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QApplication
    )
from PySide6.QtCore import Qt

# ours
from gui.filepathwidget import FilePathWidget
from gui.numericwidget import NumericWidget
from gui.form import FormWidget


class MainWindow(QMainWindow) :
    """
        Main Application window
    """

    def __init__(self, runcmd : Callable, name="pysubfixer-gui") :
        super(MainWindow, self).__init__()
        self.runcmd = runcmd
        self.resize(500, 250)
        self.setWindowTitle(name)
       
        # our path widgets
        self.videoWidget = FilePathWidget(self)
        self.subtitleWidget = FilePathWidget(self)
        self.delayWidget = NumericWidget(self)

        # execute button
        self.runbutton = QPushButton("Execute")
        self.runbutton.clicked.connect(self.onExec)

        # a nice simple layout
        mainwidget = QWidget(self)
        mainwidget.setLayout(QVBoxLayout())
        formwidget = FormWidget(mainwidget)
        formwidget.addWidget(self.tr("&video :"), self.videoWidget)
        formwidget.addWidget(self.tr("&subtitles :"), self.subtitleWidget)
        formwidget.addWidget(self.tr("&delay (seconds) :"), self.delayWidget)
        mainwidget.layout().addWidget(formwidget)
        mainwidget.layout().addWidget(self.runbutton)
        mainwidget.layout().setAlignment(Qt.AlignVCenter)
        self.setCentralWidget(mainwidget)
    
    def onExec(self) :
        command = {
            "source": self.videoWidget.path(),
            "subs"  : self.subtitleWidget.path(),
            "delay" : self.delayWidget.value()
        }
        self.runcmd(command)

def runApplication(cmd : Callable) :
    """
    Launch the application
    """
    myApp = QApplication(argv)
    try : 
        widget = MainWindow(runcmd=cmd)
        widget.show()
        myApp.exec()
    except Exception as E :
        print(f'Error : {E}')
    finally:
        myApp.Close()

