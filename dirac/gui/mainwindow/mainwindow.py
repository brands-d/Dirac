import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from .gridsettings.grid_group_box import GridSettings
from .boundarysettings.boundary_group_box import BoundarySettings
from .simulationssettings.simulation_group_box import SimulationSettings
from .initialsettings.initial_group_box import InitialSettings

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class MainWindow(QMainWindow, UI):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setup()

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
        pass
