import qdarkstyle

from PyQt5.QtWidgets import QApplication

from dirac.gui.mainwindow.mainwindow import MainWindow
from dirac import __version__, __project__


class Dirac(QApplication):

    def __init__(self, *args):
        super().__init__(*args)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    def run(self):
        main_window = MainWindow()
        main_window.show()

        return super().exec_()
