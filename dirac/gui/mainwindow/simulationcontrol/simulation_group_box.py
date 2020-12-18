import os
from time import localtime, strftime

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class SimulationControl(QWidget, UI):
    simulation_triggered = pyqtSignal()
    run_button_texts = {'locked': 'Running', 'not locked': 'Run'}

    def __init__(self):
        super(SimulationControl, self).__init__()
        self.setupUi(self)

        self.connect()

    def lock_run(self, bool):
        self.run_button.setEnabled(not bool)
        text = self.run_button_texts['locked'] if bool else \
            self.run_button_texts['not locked']

        self.run_button.setText(text)

    def get_settings(self):
        is_save = self.save_checkbox.isChecked()
        temp = self.save_lineedit.text()
        file_name = temp if temp else strftime('%Y_%m_%d_%H_%M',
                                               localtime())

        return {'is save': is_save, 'file name': file_name}

    def connect(self):
        self.run_button.clicked.connect(self.simulation_triggered.emit)
