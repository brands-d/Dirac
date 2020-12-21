import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from .gridsettings.grid_group_box import GridSettings
from .boundarysettings.boundary_group_box import BoundarySettings
from .simulationssettings.simulation_group_box import SimulationSettings
from .initialsettings.initial_group_box import InitialSettings
from ..player.player import Player
from dirac.model.model import DiracModel

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class MainWindow(QMainWindow, UI):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.stop = False
        self.player_windows = []
        self.setup()
        self.connect()

    def trigger_simulation(self):
        self.simulation_settings.lock_run(True)

        settings = self.get_settings()
        model = DiracModel(settings)
        result = model.run(callback=self.inter_loop_update)

        self.stop = False
        self.simulation_settings.lock_run(False)

        self.open_new_player(result)

    def open_new_player(self, result):
        new_player = Player(result, self.inter_process_update)
        new_player.close_triggered.connect(self.player_closed)

        self.player_windows.append(new_player)

        new_player.show()

        self.statusbar.showMessage('Finished.')

    def player_closed(self):
        player = self.sender()
        self.player_windows.remove(player)

        self.statusbar.showMessage('Player closed.')

    def inter_loop_update(self, progress):
        percent = 100 * progress
        self.statusbar.showMessage('Simulation Progress: {0:.1f}%'.format(
            percent))

        QApplication.processEvents()

        if self.stop:
            self.statusbar.showMessage('Simulation aborted at {0:.1f}%'.format(
                percent))
            return True

        return False

    def inter_process_update(self, progress):
        percent = 100 * progress
        self.statusbar.showMessage('Simulation Finished. Processing '
                                   'results: {0:.1f}%'.format(
            percent))

        QApplication.processEvents()

    def load(self, paths):
        for path in paths:
            try:
                result = DiracModel.init_from_path(path)
                self.open_new_player(result)
            except IOError:
                self.statusbar.showMessage(
                    '{} could not be loaded.'.format(path))

    def stop_simulation(self):
        self.stop = True

    def get_settings(self):
        settings = {}
        widgets = [self.grid_settings, self.boundary_settings,
                   self.simulation_settings, self.initial_settings]

        for widget in widgets:
            settings.update(widget.get_settings())

        return settings

    def closeEvent(self, event):
        for player in self.player_windows:
            player.blockSignals(True)
            player.close()

        event.accept()

    def setup(self):
        self.grid_settings = GridSettings()
        self.boundary_settings = BoundarySettings()
        self.simulation_settings = SimulationSettings()
        self.initial_settings = InitialSettings()

        self.central_widget.layout().addWidget(self.grid_settings)
        self.central_widget.layout().addWidget(self.boundary_settings)
        self.central_widget.layout().addWidget(self.initial_settings)
        self.central_widget.layout().addWidget(self.simulation_settings)

    def connect(self):
        self.simulation_settings.simulation_triggered.connect(
            self.trigger_simulation)
        self.simulation_settings.simulation_stop_triggered.connect(
            self.stop_simulation)
        self.simulation_settings.load_triggered.connect(self.load)
