#! /usr/env python
# gui/filepathwidget.py : widget for picking input files 

# python
import shlex

# QT
from PySide6.QtWidgets import QStackedWidget, QPushButton, QProgressBar

# ours
from ffmpeg import fix_subs

class RunButton(QStackedWidget) :
    """
        nice button to run a command
    """

    _video  : str = ""
    _subs   : str = ""
    _delay  : int = 0
    _output : str = ""

    @property
    def arguments(self) -> dict :
        return {
        "video" : self._video,
        "subs" : self._subs, 
        "delay" : self._delay, 
        "output": self._output
        }

    @arguments.setter
    def arguments(self, args : dict) :
        prev = self.arguments
        prev.update(args)
        self.update()

    def update(self) :
        # update subwidgets:
        self._button.setText(self.get_label())
        self._progressbar.setRange(0, 0 if self.__clicked else 1)
        # set correct visibility :
        self.setCurrentWidget(self._progressbar if self.__clicked else self._button)

    def on_finished(self):
        # Stop the pulsation
        self._progressbar.setRange(0,1)
        self.update()

    def get_label(self) -> str :
        if self.__clicked :
            return self.tr("&FFMpeg Running, please wait")
        else :
            return self.tr("Run FFMpeg")

    def get_tooltip(self) -> str :
        if self.__clicked :
            return self.tr("&Running the correct ffmpeg sequence, don't worry")
        else :
            return self.tr("&click to embed ") + self._str + self.tr("& into") + self._video

    def __init__(self, parent) : 
        super().__init__(parent)
        self.__clicked = False
        # add subwidgets :
        self._button = QPushButton()
        self._progressbar = QProgressBar()
        self.addWidget(self._button)
        self.addWidget(self._progressbar)
        # update appearance :
        self.update()
        # on clicked :
        self._button.clicked.connect(self._on_exec)

    def _on_exec(self) :
        self.__ffmpeg = fix_subs(
            subs  = self._subs,
            video = self._video,
            delay = self._delay,
            output = self._output,
            on_finished=self.on_finished)
        