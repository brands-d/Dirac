import h5py
import numpy as np

from dirac import __directory__
from dirac.library.spinor import Spinor
from .dirac_solver import DiracSolver


class DiracModel:

    def __init__(self, settings):
        self.settings = settings

    def run(self, callback=None):
        dx, dy, dt = [self.settings[key] for key in ('dt', 'dx', 'dy')]
        time_steps = self.settings['time steps']
        s0 = self.construct_initial_spinor()

        solver = DiracSolver(s0, time_steps, delta=(dx, dy, dt))
        result = solver.solve(callback=callback)

        self.save_results(result)
        return result

    def construct_initial_spinor(self):
        shape = [self.settings[key] for key in ('M', 'N')]
        delta = [self.settings[key] for key in ('dx', 'dy')]
        periodic = self.settings['boundary condition']
        x, y = Spinor.get_meshgrid(shape, delta)
        gauss = np.exp(-(x**2 + y**2) / 5)

        return Spinor(gauss, np.zeros(gauss.shape), periodic=periodic)

    def save_results(self, result):
        if self.settings['is save']:
            path = __directory__ / '../output' / self.settings['file name']
            with h5py.File(str(path), 'w') as file:
                file.create_dataset(result)
                pass
