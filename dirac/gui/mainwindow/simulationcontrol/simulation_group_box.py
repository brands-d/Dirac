import os
from time import localtime, strftime

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class SimulationControl(QWidget, UI):
    simulation_triggered = pyqtSignal()
    simulation_stop_triggered = pyqtSignal()

    def __init__(self):
        super(SimulationControl, self).__init__()
        self.setupUi(self)

        self.connect()

    def lock_run(self, state):
        self.run_button.clicked.disconnect()

        if state:
            text = 'Cancel'
            self.run_button.clicked.connect(
                self.simulation_stop_triggered.emit)
        else:
            text = 'Run'
            self.run_button.clicked.connect(self.simulation_triggered.emit)

        self.run_button.setText(text)
        self.run_button.repaint()

    def get_settings(self):
        is_save = self.save_checkbox.isChecked()
        temp = self.save_lineedit.text()
        file_name = temp if temp else strftime('%Y_%m_%d_%H_%M',
                                               localtime())

        return {'is save': is_save, 'file name': file_name}

    def connect(self):
        self.run_button.clicked.connect(self.simulation_triggered.emit)
