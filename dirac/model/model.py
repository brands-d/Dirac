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
        m, V = self.construct_m(), self.construct_V()
        s0 = self.construct_initial_spinor()

        solver = DiracSolver(s0, m, V, time_steps, dt=dt)
        result = solver.solve(callback=callback)
        self.save_results(result)

        return result

    def construct_m(self):
        m = self.settings['m']
        m_step = self.settings['m_step']
        if m_step is not None:
            def m_func(x):
                values = np.zeros(x.shape)
                values[x > m_step] = m
                return values

        else:
            def m_func(x):
                values = m * np.ones(x.shape)
                return values

        return m_func

    def construct_V(self):
        V = self.settings['V']
        V_step = self.settings['V_step']
        if V_step is not None:
            def V_func(x):
                values = np.zeros(x.shape)
                values[x > V_step] = V
                return values

        else:
            def V_func(x):
                values = V * np.ones(x.shape)
                return values

        return V_func

    def construct_initial_spinor(self):
        m = self.settings['m']
        k_x, k_y = self.settings['k']
        shape = self.settings['shape']
        range = self.settings['range']
        periodic = self.settings['periodic']
        mu_x, mu_y = self.settings['position']
        sigma_x, sigma_y = self.settings['sigma']

        x, y = Spinor.get_meshgrid(range, shape)
        gauss = np.exp(-((x - mu_x)**2 / (2 * sigma_x**2) +
                         (y - mu_y)**2 / (2 * sigma_y**2)))

        v = (cmath.sqrt(k_x**2 + k_y**2 - m**2) - 1j * m) / (k_y + 1j * k_x) \
            if (k_y + 1j * k_x) != 0 else 0

        return Spinor(gauss, v * gauss, range, periodic=periodic)

    def save_results(self, result):
        if self.settings['is save']:
            path = __directory__ / '../output'
            if not os.path.exists(path):
                os.makedirs(path)

            path = path / self.settings['file name']
            with GzipFile(path, 'wb') as file:
                pickle.dump(result, file)
