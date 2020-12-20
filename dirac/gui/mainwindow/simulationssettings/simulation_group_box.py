import os
from time import localtime, strftime

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class SimulationSettings(QWidget, UI):
    simulation_triggered = pyqtSignal()
    simulation_stop_triggered = pyqtSignal()
    load_triggered = pyqtSignal(list)

    def __init__(self):
        super(SimulationSettings, self).__init__()
        self.setupUi(self)

        self.connect()

    def get_settings(self):
        time_steps = self.time_steps_spinbox.value()
        dt = self.dt_spinbox.value()
        is_save = self.save_checkbox.isChecked()
        temp = self.save_lineedit.text()
        file_name = temp if temp else strftime('%Y_%m_%d_%H_%M', localtime())

        return {'time steps': time_steps, 'dt': dt, 'is save': is_save,
                'file name': file_name}

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

    def load(self):
        start_path = __directory__ / '../output'
        paths, _ = QFileDialog.getOpenFileNames(None, 'Open file(s)',
                                                str(start_path))

        self.load_triggered.emit(paths)

    def connect(self):
        self.run_button.clicked.connect(self.simulation_triggered.emit)
        self.load_button.clicked.connect(self.load)
