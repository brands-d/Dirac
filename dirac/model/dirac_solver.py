from copy import deepcopy

import time
import numpy as np

from dirac.library.spinor import *


class DiracSolver:

    def __init__(self, s0, m, V, num, dt=1):
        self.spinor = s0
        self.dt = self.calc_t_cfl() * dt
        self.n_u, self.n_v = s0.get_neighbours()
        self.r_x, self.r_y = self.dt / s0.dx, self.dt / s0.dy

        self.times = np.arange(0, num) * self.dt
        self.k_u, self.k_v = self.calc_pre_factors(m, V)

    def calc_t_cfl(self):
        return (1 / self.spinor.dx + 1 / self.spinor.dy)**(-1)

    def solve(self, callback=None):
        results = []

        for i, t in enumerate(self.times):
            if callback is not None:
                is_stop = callback(i / len(self.times))
                if is_stop:
                    break

            results.append([t, deepcopy(self.spinor)])
            self.advance_u()
            self.advance_v()

        return results

    def advance_u(self):
        self.spinor.u *= self.k_u[0]
        self.spinor.u -= 1j * self.r_x * (self.spinor.v[self.n_u[2]]
                                          - self.spinor.v[self.n_u[3]])
        self.spinor.u -= self.r_y * (self.spinor.v[self.n_u[0]]
                                     - self.spinor.v[self.n_u[1]])
        self.spinor.u *= self.k_u[1]

    def advance_v(self):
        self.spinor.v *= self.k_v[0]
        self.spinor.v += 1j * self.r_x * (self.spinor.u[self.n_v[2]]
                                          - self.spinor.u[self.n_v[3]])
        self.spinor.v -= self.r_y * (self.spinor.u[self.n_v[0]]
                                     - self.spinor.u[self.n_v[1]])
        self.spinor.v *= self.k_v[1]

    def calc_pre_factors(self, m, V):
        ihc = 1j
        x_u, y_u = self.spinor.u.get_space_points()
        x_v, y_v = self.spinor.v.get_space_points()

        def sigma(x, y):
            border = 0.75
            values = np.zeros(x.shape, dtype=np.complex_)
            values[abs(x) > border] = 50 * (
                    abs(x[abs(x) > border]) - border)**4
            values[abs(y) > border] = 50 * (
                    abs(x[abs(x) > border]) - border)**4
            return values

        temp = (m(x_u) + V(x_u)) / ihc - sigma(x_u,y_u)
        k_u = [1 + temp * self.dt / 2, (1 - temp * self.dt / 2)**(-1)]

        temp = (V(x_v) - m(x_v)) / ihc - sigma(x_v,y_v)
        k_v = [1 + temp * self.dt / 2, (1 - temp * self.dt / 2)**(-1)]

        return k_u, k_v
