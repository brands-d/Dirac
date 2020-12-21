import os
import time

import pyqtgraph.exporters as ex

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QRectF
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from .export.exportbox import Export
from .information.informationbox import Information
from .playercontrol.playercontrol import PlayerControl
from .plot.plot import *
from .viewsettings.viewsettings import ViewSettings
from dirac import __directory__

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Player(QWidget, UI):
    close_triggered = pyqtSignal()

    def __init__(self, result, callback):
        super(QWidget, self).__init__()
        self.setupUi(self)

        self.range = result[0][1].range
        self.shape = result[0][1].shape
        self.delta = (result[0][1].dx, result[0][1].dx)
        self.x = result[0][1].u.get_x_axis(self.range, self.shape[1])
        self.y = result[0][1].u.get_y_axis(self.range, self.shape[0])
        self.result = self.process_results(result, callback)
        self.current_idx = 0
        self.exporter = None

        self.setup()
        self.connect()

        self.set_image(self.current_idx)

    def process_results(self, results, callback):
        proc_results = []
        for i, result in enumerate(results):
            callback(i / len(results))
            proc_results.append([result[0], abs(result[1])])

        return proc_results

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

        self.set_exporter()
        self.set_image(self.current_idx)

    def set_exporter(self):
        self.exporter = ex.ImageExporter(self.plot.get_plot_item())

    def set_image(self, idx):
        time, spinor = self.result[idx]
        self.plot.plot(spinor, self.range)

        self.information.set_current_idx(idx, len(self.result))
        self.information.set_current_time(time)

    def export_movie(self):
        self.set_image(0)
        self.current_idx = 0
        for i, _ in enumerate(self.result):
            self.next()
            self.export_image()

        path = __directory__ / '../output'
        os.system('ffmpeg -i {0}/%d.png  {0}/output.mp4'.format(str(path)))

        for i in range(len(self.result)):
            os.system('rm {0}/{1:.0f}.png'.format(path, i))

    def export_image(self):
        path = __directory__ / '../output'
        if not os.path.exists(path):
            os.makedirs(path)

        plot_item = self.plot.get_plot_item()
        height = plot_item.sceneBoundingRect().height()
        square_rect = QRectF(0, 0, height, height)
        plot_item.scene().setSceneRect(square_rect)
        self.exporter.parameters()['height'] = 2000
        self.exporter.parameters()['width'] = 2000

        path = path / '{0:.0f}.png'.format(self.current_idx)
        self.exporter.export(str(path))

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

        self.set_exporter()

    def connect(self):
        self.player_control.next_triggered.connect(self.next)
        self.player_control.previous_triggered.connect(self.previous)
        self.player_control.start_triggered.connect(self.start)
        self.player_control.stop_triggered.connect(self.stop)
        self.view.plot_toggled.connect(self.toggle_plot_type)
        self.export.save_image_triggered.connect(self.export_image)
        self.export.save_movie_triggered.connect(self.export_movie)
