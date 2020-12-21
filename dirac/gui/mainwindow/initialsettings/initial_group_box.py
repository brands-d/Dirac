import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class InitialSettings(QWidget, UI):

    def __init__(self):
        super(InitialSettings, self).__init__()
        self.setupUi(self)

        self.connect()

    def get_settings(self):
        position = [self.position_x_spinbox.value(),
                    self.position_y_spinbox.value()]
        k = [self.k_x_spinbox.value(),
             self.k_y_spinbox.value()]
        sigma = [self.sigma_x_spinbox.value(),
                 self.sigma_y_spinbox.value()]
        m = self.m_spinbox.value()
        V = self.V_spinbox.value()
        m_step = self.m_step_spinbox.value() if \
            self.m_step_checkbox.isChecked() else None
        V_step = self.V_step_spinbox.value() if \
            self.V_step_checkbox.isChecked() else None

        return {'position': position, 'sigma': sigma, 'k': k,
                'm': m, 'V': V, 'm_step': m_step, 'V_step': V_step}

    def connect(self):
        self.m_step_checkbox.stateChanged.connect(
            self.m_step_spinbox.setEnabled)
        self.V_step_checkbox.stateChanged.connect(
            self.V_step_spinbox.setEnabled)
