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
        pml = None

        solver = DiracSolver(s0, m, V, time_steps, pml=pml, dt=dt, c=c)
        result = solver.solve(callback=callback)
        self.save_results(result)

        return result

    def construct_pml(self):
        if self.settings['pml']:
            l_border = (1 - self.settings['x thickness']) * \
                       self.settings['range'][0][0]
            r_border = (1 - self.settings['x thickness']) * \
                       self.settings['range'][0][1]
            order = self.settings['x order']
            order = self.settings['x factor']

            def sigma_x(x):
                values = np.zeros(x.shape, dtype=np.complex_)
                values[x >= r_border] = factor * (
                        x[x >= r_border] - r_border)**order
                values[x < l_border] = factor * (
                        x[x < l_border] - l_border)**order
                return values

            t_border = (1 - self.settings['y thickness']) * \
                       self.settings['range'][1][1]
            b_border = (1 - self.settings['y thickness']) * \
                       self.settings['range'][1][0]
            order = self.settings['y order']
            factor = self.settings['y factor']

            def sigma_y(y):
                values = np.zeros(y.shape, dtype=np.complex_)
                values[y >= t_border] = factor * (
                        y[y >= t_border] - t_border)**order
                values[y < b_border] = factor * (
                        y[y < b_border] - b_border)**order

                return values

            return [sigma_x, sigma_y]

        else:
            return None

    def construct_m(self):
        m = self.settings['simulation']['m']
        # m_step = self.settings['m_step']
        m_step = None
        if m_step is not None:
            def m_func(x):
                values = np.zeros(x.shape)
                values[x >= m_step] = m
                return values

        else:
            def m_func(x):
                values = m * np.ones(x.shape)
                return values

        return m_func

    def construct_V(self):
        V = self.settings['simulation']['V']
        # V_step = self.settings['V_step']
        V_step = None
        if V_step is not None:
            def V_func(x):
                values = np.zeros(x.shape)
                values[x >= V_step] = V
                return values

        else:
            def V_func(x):
                values = V * np.ones(x.shape)
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
