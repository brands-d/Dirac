import os
import cmath
import pickle
from gzip import GzipFile

import numpy as np

from dirac import __directory__
from dirac.library.spinor import Spinor
from .dirac_solver import DiracSolver


class DiracModel:

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def init_from_path(cls, path):
        try:
            with GzipFile(path, 'rb') as file:
                result = pickle.load(file)

            return result
        except:
            raise IOError

    def run(self, callback=None):
        dt = self.settings['dt']
        time_steps = self.settings['time steps']
        m = 1
        V = lambda x, y: 2 * np.zeros(x.shape)
        s0 = self.construct_initial_spinor(m)

        solver = DiracSolver(s0, m, V, time_steps, dt=dt)
        result = solver.solve(callback=callback)
        self.save_results(result)

        return result

    def construct_initial_spinor(self, m):
        shape = self.settings['shape']
        range = self.settings['range']
        periodic = self.settings['periodic']
        x, y = Spinor.get_meshgrid(range, shape)
        gauss = np.exp(-(x**2 + y**2) / 0.05)

        u = 1
        k_x = 1
        k_y = 1
        k_2 = k_x**2 + k_y**2
        v = (cmath.sqrt(k_2 - m**2) - 1j * m) / (k_y + 1j * k_x)

        return Spinor(u * gauss, v * gauss, range, periodic=periodic)

    def save_results(self, result):
        if self.settings['is save']:
            path = __directory__ / '../output'
            if not os.path.exists(path):
                os.makedirs(path)

            path = path / self.settings['file name']
            with GzipFile(path, 'wb') as file:
                pickle.dump(result, file)
