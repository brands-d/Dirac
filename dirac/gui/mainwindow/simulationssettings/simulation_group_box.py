import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class SimulationSettings(QWidget, UI):

    def __init__(self):
        super(SimulationSettings, self).__init__()
        self.setupUi(self)

    def get_settings(self):
        time_steps = self.time_steps_spinbox.value()
        dt = self.dt_spinbox.value()
        dx = self.dx_spinbox.value()
        dy = self.dy_spinbox.value()

        return {'time steps': time_steps, 'dt': dt, 'dx': dx, 'dy': dy}
