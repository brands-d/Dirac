import os
from time import localtime, strftime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from ..player.player import Player
from dirac.model.model import DiracModel

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class MainWindow(QMainWindow, UI):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.stop = False
        self.player_windows = []
        self.connect()

    def trigger_simulation(self):
        settings = self.get_settings()
        model = DiracModel(settings)
        result = model.run(callback=self.inter_loop_update)

        self.stop = False

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

    def load(self):
        path = self.save_lineedit.text()
        if path:
            try:
                result = DiracModel.init_from_path(path)
                self.open_new_player(result)
            except IOError:
                self.statusbar.showMessage(
                    '{} could not be loaded.'.format(path))

    def stop_simulation(self):
        self.stop = True

    def get_settings(self):
        active = self.active_checkbox.isChecked()
        factor = self.factor_spinbox.value()
        order = self.order_spinbox.value()
        thickness = self.thickness_spinbox.value() / 100
        abc = {'active': active, 'order': order,
                   'factor': factor, 'thickness': thickness}

        num = self.grid_spinbox.value()
        grid = {'num': num}

        position = [self.position_x_spinbox.value(),
                    self.position_y_spinbox.value()]
        k = [self.k_x_spinbox.value(), self.k_y_spinbox.value()]
        sigma = [self.sigma_x_spinbox.value(), self.sigma_y_spinbox.value()]
        initial = {'position': position, 'sigma': sigma, 'k': k}

        time_steps = self.time_steps_spinbox.value()
        dt = self.dt_spinbox.value()
        c = self.c_spinbox.value()
        is_save = self.save_checkbox.isChecked()
        temp = self.save_lineedit.text()
        file_name = temp if temp else strftime('%Y_%m_%d_%H_%M', localtime())
        m = self.m_spinbox.value()
        V = self.V_spinbox.value()
        m_step = self.m_step_checkbox.isChecked()
        V_step = self.V_step_checkbox.isChecked()
        simulation = {'time steps': time_steps, 'dt': dt, 'is save': is_save,
                      'file name': file_name, 'c': c, 'm': m, 'V': V,
                      'm_step': m_step, 'V_step': V_step}

        return {'abc': abc, 'grid': grid, 'initial': initial,
                'simulation': simulation}

    def closeEvent(self, event):
        for player in self.player_windows:
            player.blockSignals(True)
            player.close()

        event.accept()

    def connect(self):
        self.run_button.clicked.connect(self.trigger_simulation)
        self.load_button.clicked.connect(self.load)
