import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class GridSettings(QWidget, UI):

    def __init__(self):
        super(GridSettings, self).__init__()
        self.setupUi(self)

        self.connect()

    def change_N(self, N):
        if N % 2 != 0:
            self.N_spinbox.blockSignals(True)
            self.N_spinbox.setValue(N + 1)
            self.N_spinbox.blockSignals(False)

    def change_M(self, M):
        if M % 2 != 0:
            self.M_spinbox.blockSignals(True)
            self.M_spinbox.setValue(M + 1)
            self.M_spinbox.blockSignals(False)

    def change_x_min(self, value):
        if value >= self.x_max_spinbox.value():
            self.x_max_spinbox.blockSignals(True)
            step = self.x_max_spinbox.singleStep()
            self.x_max_spinbox.setValue(value + step)
            self.x_max_spinbox.blockSignals(False)

    def change_x_max(self, value):
        if value <= self.x_min_spinbox.value():
            self.x_min_spinbox.blockSignals(True)
            step = self.x_min_spinbox.singleStep()
            self.x_min_spinbox.setValue(value - step)
            self.x_min_spinbox.blockSignals(False)

    def change_y_min(self, value):
        if value >= self.y_max_spinbox.value():
            self.y_max_spinbox.blockSignals(True)
            step = self.y_max_spinbox.singleStep()
            self.y_max_spinbox.setValue(value + step)
            self.y_max_spinbox.blockSignals(False)

    def change_y_max(self, value):
        if value <= self.y_min_spinbox.value():
            self.y_min_spinbox.blockSignals(True)
            step = self.y_min_spinbox.singleStep()
            self.y_min_spinbox.setValue(value - step)
            self.y_min_spinbox.blockSignals(False)

    def get_settings(self):
        N = self.N_spinbox.value()
        M = self.M_spinbox.value()
        x_min = self.x_min_spinbox.value()
        x_max = self.x_max_spinbox.value()
        y_min = self.y_min_spinbox.value()
        y_max = self.y_max_spinbox.value()

        return {'shape': (M, N), 'range': ((x_min, x_max), (y_min, y_max))}

    def connect(self):
        self.N_spinbox.valueChanged.connect(self.change_N)
        self.M_spinbox.valueChanged.connect(self.change_M)
        self.x_min_spinbox.valueChanged.connect(self.change_x_min)
        self.x_max_spinbox.valueChanged.connect(self.change_x_max)
        self.y_min_spinbox.valueChanged.connect(self.change_y_min)
        self.y_max_spinbox.valueChanged.connect(self.change_y_max)
