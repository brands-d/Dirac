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

    def start(self):
        if self.start_button.text() == 'Start':
            self.start_button.setText('Stop')
            self.start_triggered.emit()

        else:
            self.start_button.setText('Start')
            self.stop_triggered.emit()

    def get_fps(self):
        return self.fps_spinbox.value()

    def connect(self):
        self.next_button.clicked.connect(self.next_triggered.emit)
        self.previous_button.clicked.connect(self.previous_triggered.emit)
        self.start_button.clicked.connect(self.start)
