import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Export(QWidget, UI):
    save_image_triggered = pyqtSignal()
    save_movie_triggered  =pyqtSignal()

    def __init__(self):
        super(Export, self).__init__()
        self.setupUi(self)

        self.exporter = None

        self.connect()

    def connect(self):
        self.save_image.clicked.connect(self.save_image_triggered.emit)
        self.save_movie.clicked.connect(self.save_movie_triggered.emit)