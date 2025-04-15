import sys
from main import main
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel
from PyQt6.QtCore import Qt

class DelayInputWidget(QWidget) :
    def __init__(self, parent = None) :
        super(DelayInputWidget, self).__init__(parent)
        self.textbox = QLineEdit("0")
        #self.textbox.setValidator(Qt.QIntValidator())
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(QLabel("Delay :"))
        horizontalLayout.addWidget(self.textbox)
        self.setLayout(horizontalLayout)

    def get_time(self) -> int :
        return int(self.textbox.text())

class PathInputWidget(QWidget) :
    def __init__(self, name : str, parent = None) :
        super(PathInputWidget, self).__init__(parent)
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
        

class MainWidget(QMainWindow) :
    def __init__(self, name="pysubfixer-gui") :
        super(MainWidget, self).__init__()

        self.resize(500, 250)
        self.setWindowTitle(name)
       
        # our path widgets
        self.videoWidget = PathInputWidget("Video")
        self.subtitleWidget = PathInputWidget("Subtitle")
        self.delayWidget = DelayInputWidget()

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
        main(command)


myApp = QApplication(sys.argv)
widget = MainWidget()
widget.show()
myApp.exec()