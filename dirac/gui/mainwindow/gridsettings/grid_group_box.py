import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class GridSettings(QWidget, UI):

    def __init__(self):
        super(GridSettings, self).__init__()
        self.setupUi(self)