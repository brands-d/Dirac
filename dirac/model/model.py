import os
import cmath
import pickle
from gzip import GzipFile

import numpy as np

from dirac import __directory__
from dirac.library.spinor import Spinor
from dirac.library.misc import *
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
        dt = self.settings['simulation']['dt']
        c = self.settings['simulation']['c']
        time_steps = self.settings['simulation']['time steps']
        m = self.construct_m()
        V = self.construct_V()
        s0 = self.construct_initial_spinor()
        abc = self.construct_abc()

        solver = DiracSolver(s0, m, V, time_steps, abc=abc, dt=dt, c=c)
        result = solver.solve(callback=callback)
        self.save_results(result)

        return result

    def construct_abc(self):
        if self.settings['abc']['active']:
            r_border = 1 - self.settings['abc']['thickness']
            l_border = self.settings['abc']['thickness'] - 1
            order = self.settings['abc']['order']
            factor = self.settings['abc']['factor']

            def sigma(x):
                values = np.zeros(x.shape, dtype=np.complex_)
                values[x >= r_border] = factor * (
                        x[x >= r_border] - r_border)**order
                values[x < l_border] = factor * (
                        x[x < l_border] - l_border)**order
                return values

            return sigma

        else:
            return None

    def construct_m(self):
        m = self.settings['simulation']['m']
        m_step = self.settings['simulation']['m_step']

        if m_step is True:
            def m_func(x):
                values = np.zeros((len(x), len(x)))
                values[x.flatten() >= 0] = m
                return values

        else:
            def m_func(x):
                values = m * np.ones((len(x), len(x)))
                return values

        return m_func

    def construct_V(self):
        V = self.settings['simulation']['V']
        V_step = self.settings['simulation']['V_step']

        if V_step is True:
            def V_func(x):
                values = np.zeros((len(x), len(x)))
                values[x.flatten() >= 0, :] = V
                return values

        else:
            def V_func(x):
                values = V * np.ones((len(x), len(x)))
                return values

        return V_func

    def construct_initial_spinor(self):
        c = self.settings['simulation']['c']
        m = self.settings['simulation']['m'] / c
        k_x, k_y = self.settings['initial']['k']
        omega = cmath.sqrt(m**2 + k_x**2 + k_y**2)
        num = self.settings['grid']['num']
        mu_x, mu_y = self.settings['initial']['position']
        sigma_x, sigma_y = self.settings['initial']['sigma']

        # Space (2D Gaussian)
        x, y = get_mesh(num)
        gauss = np.exp(-((x - mu_x)**2 / (2 * sigma_x**2) +
                         (y - mu_y)**2 / (2 * sigma_y**2)))
        space = gauss * np.exp(1j * (k_x * x + k_y * y))

        # Momentum (Plane Wave with u0 = 1)
        if k_x == 0 and k_y == 0 and m == 0:
            v = 0

        else:
            v = (k_y - 1j * k_x) / (omega + m)

        return Spinor(space, v * space)

    def save_results(self, result):
        if self.settings['simulation']['is save']:
            path = __directory__ / '../output'
            if not os.path.exists(path):
                os.makedirs(path)

            path = path / self.settings['simulation']['file name']
            with GzipFile(path, 'wb') as file:
                pickle.dump(result, file)
