import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class PlayerControl(QWidget, UI):
    next_triggered = pyqtSignal()
    start_triggered = pyqtSignal()
    stop_triggered = pyqtSignal()
    previous_triggered = pyqtSignal()

    def __init__(self):
        super(PlayerControl, self).__init__()
        self.setupUi(self)

        self.connect()

    def connect(self):
        self.next_button.clicked.connect(self.next_triggered.emit)
        self.previous_button.clicked.connect(self.previous_triggered.emit)
