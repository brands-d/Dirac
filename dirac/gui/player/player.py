import os
import time

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from .export.exportbox import Export
from .information.informationbox import Information
from .playercontrol.playercontrol import PlayerControl
from .plot.plot import *
from .viewsettings.viewsettings import ViewSettings

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Player(QWidget, UI):
    close_triggered = pyqtSignal()

    def __init__(self, result):
        super(QWidget, self).__init__()
        self.setupUi(self)

        self.range = result[0][1].range
        self.shape = result[0][1].shape
        self.delta = (result[0][1].dx, result[0][1].dx)
        self.x = result[0][1].u.get_x_axis(self.range, self.shape[1])
        self.y = result[0][1].u.get_y_axis(self.range, self.shape[0])
        self.result = [[t, abs(s)] for t, s in result]
        self.current_idx = 0

        self.setup()
        self.connect()

        self.set_image(self.current_idx)

    def next(self):
        if self.current_idx < len(self.result) - 1:
            self.current_idx += 1
        else:
            self.current_idx = 0

        self.set_image(self.current_idx)

    def previous(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        else:
            self.current_idx = len(self.result) - 1

        self.set_image(self.current_idx)

    def stop(self):
        self.is_play = False

    def start(self):
        self.is_play = True

        while self.is_play:
            start_time = time.time()

            self.next()
            QApplication.processEvents()

            duration = time.time() - start_time
            fps = self.player_control.get_fps()
            sleep = 1 / fps - duration
            if sleep >= 0:
                time.sleep(sleep)

    def toggle_plot_type(self):
        layout = self.widget.layout()
        layout.removeWidget(self.plot)
        self.plot.deleteLater()

        if isinstance(self.plot, SurfacePlot):
            self.plot = ImagePlot(layout, self.range)
        else:
            self.plot = SurfacePlot(layout, self.x, self.y)

        self.set_image(self.current_idx)

    def set_image(self, idx):
        time, spinor = self.result[idx]
        self.plot.plot(spinor, self.range)

        self.information.set_current_idx(idx, len(self.result))
        self.information.set_current_time(time)

    def closeEvent(self, event):
        self.is_play = False
        self.close_triggered.emit()
        event.accept()

    def setup(self):
        self.plot = ImagePlot(self.widget.layout(), self.range)
        self.player_control = PlayerControl()
        self.information = Information()
        self.export = Export()
        self.view = ViewSettings()

        layout = QVBoxLayout()
        self.widget.layout().addLayout(layout)
        layout.addWidget(self.player_control)
        layout.addWidget(self.information)
        layout.addWidget(self.view)
        layout.addWidget(self.export)

    def connect(self):
        self.player_control.next_triggered.connect(self.next)
        self.player_control.previous_triggered.connect(self.previous)
        self.player_control.start_triggered.connect(self.start)
        self.player_control.stop_triggered.connect(self.stop)
        self.view.plot_toggled.connect(self.toggle_plot_type)
