import os
import time

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QRectF, Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
import pyqtgraph.exporters as ex

from dirac import __directory__
from dirac.gui.player.plot import *

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Player(QWidget, UI):
    close_triggered = pyqtSignal()

    def __init__(self, result, callback):
        super(QWidget, self).__init__()
        self.setupUi(self)

        self.num = result[0][1].num
        self.ds = result[0][1].ds
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

    def get_fps(self):
        return self.fps_spinbox.value()

    def next(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            step_size = 10
        else:
            step_size = 1

        self.current_idx = (self.current_idx + step_size) % len(self.result)

        self.set_image(self.current_idx)

    def previous(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            step_size = 10
        else:
            step_size = 1

        self.current_idx = self.current_idx - step_size

        if self.current_idx < 0:
            self.current_idx = len(self.result) + self.current_idx

        self.set_image(self.current_idx)

    def run(self):
        if self.start_button.text() == 'Start':
            self.start()

        else:
            self.stop()

    def stop(self):
        self.start_button.setText('Start')
        self.is_play = False

    def start(self):
        self.start_button.setText('Stop')
        self.is_play = True

        while self.is_play:
            start_time = time.time()

            self.next()
            QApplication.processEvents()

            duration = time.time() - start_time
            fps = self.get_fps()
            sleep = 1 / fps - duration
            if sleep >= 0:
                time.sleep(sleep)

    def toggle_plot_type(self):
        self.plot_layout.removeWidget(self.plot)
        self.plot.deleteLater()

        if isinstance(self.plot, SurfacePlot):
            self.plot = ImagePlot(self.plot_layout)
            self.set_exporter()
        else:
            self.plot = SurfacePlot(self.plot_layout)

        self.set_image(self.current_idx)

    def set_exporter(self):
        self.exporter = ex.ImageExporter(self.plot.get_plot_item())

    def set_image(self, idx):
        time, spinor = self.result[idx]
        self.plot.plot(spinor)

        self.set_current_idx(idx, len(self.result))
        self.set_current_time(time)

    def set_current_idx(self, idx, max_):
        text = '{0:.0f} / {1:.0f}'.format(idx, max_)
        self.idx_label.setText(text)

    def set_current_time(self, time):
        text = '{0:.3f} a.u.'.format(time)
        self.time_label.setText(text)

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
        if isinstance(self.plot, SurfacePlot):
            self.toggle_plot_type()

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
        self.plot = ImagePlot(self.plot_layout)
        self.set_exporter()

    def connect(self):
        self.surface_radiobutton.clicked.connect(self.toggle_plot_type)
        self.image_radiobutton.clicked.connect(self.toggle_plot_type)
        self.save_image.clicked.connect(self.export_image)
        self.save_movie.clicked.connect(self.export_movie)
        self.start_button.clicked.connect(self.run)
        self.next_button.clicked.connect(self.next)
        self.previous_button.clicked.connect(self.previous)
