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

    def get_settings(self):
        N = self.N_spinbox.value()
        M = self.M_spinbox.value()

        return {'N': N, 'M': M}

    def connect(self):
        self.N_spinbox.valueChanged.connect(self.change_N)
        self.M_spinbox.valueChanged.connect(self.change_M)
