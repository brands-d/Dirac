import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class ViewSettings(QWidget, UI):
    plot_toggled = pyqtSignal()

    def __init__(self):
        super(ViewSettings, self).__init__()
        self.setupUi(self)

        self.connect()


    def connect(self):
        self.surface_radiobutton.clicked.connect(self.plot_toggled.emit)
        self.image_radiobutton.clicked.connect(self.plot_toggled.emit)