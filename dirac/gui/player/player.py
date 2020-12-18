import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from .export.exportbox import Export
from .information.informationbox import Information
from .playercontrol.playercontrol import PlayerControl
from .plot.plot import SurfacePlot
from dirac.model.model import DiracModel

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Player(QWidget, UI):
    close_triggered = pyqtSignal()

    def __init__(self, result):
        super(QWidget, self).__init__()
        self.setupUi(self)

        self.result = result
        self.current_idx = 0

        self.setup()
        self.connect()

        self.set_image(self.current_idx)

    def setup(self):
        self.player_control = PlayerControl()
        self.information = Information()
        self.export = Export()
        # self.plot = SurfacePlot()

        # self.setLayout(QHBoxLayout())
        # self.layout().addWidget(self.plot)
        layout = QVBoxLayout()
        self.layout().addLayout(layout)
        layout.addWidget(self.player_control)
        layout.addWidget(self.information)
        layout.addWidget(self.export)

    def next(self):
        if self.current_idx < len(self.result) - 1:
            self.current_idx += 1
            self.set_image(self.current_idx)

    def previous(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.set_image(self.current_idx)

    def set_image(self, idx):
        time, spinor = self.result[idx]
        self.plot.plot(spinor)
        self.information.set_current_idx(idx, len(self.result))
        self.information.set_current_time(time)

    def closeEvent(self, event):
        self.close_triggered.emit()
        event.accept()

    def connect(self):
        self.player_control.next_triggered.connect(self.next)
        self.player_control.previous_triggered.connect(self.previous)
