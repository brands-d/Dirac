import os
from gzip import GzipFile
import pickle

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
        s0 = self.construct_initial_spinor()

        solver = DiracSolver(s0, time_steps, dt=dt)
        result = solver.solve(callback=callback)
        self.save_results(result)

        return result

    def construct_initial_spinor(self):
        shape = self.settings['shape']
        range = self.settings['range']
        periodic = self.settings['periodic']
        x, y = Spinor.get_meshgrid(range, shape)
        gauss = np.exp(-(x**2 + y**2) / 0.05)
        
        return Spinor(gauss, np.zeros(gauss.shape), range, periodic=periodic)

    def save_results(self, result):
        if self.settings['is save']:
            path = __directory__ / '../output'
            if not os.path.exists(path):
                os.makedirs(path)

            path = path / self.settings['file name']
            with GzipFile(path, 'wb') as file:
                pickle.dump(result, file)
