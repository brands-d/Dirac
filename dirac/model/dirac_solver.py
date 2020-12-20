from copy import deepcopy

import time
import numpy as np

from dirac.library.spinor import *


class DiracSolver:

    def __init__(self, s0, num, delta=(0.1, 1, 1)):
        self.spinor = s0
        percent_t_cfl, dx, dy = delta

        self.n_u, self.n_v = s0.get_neighbours()

        m = lambda x, y: 20 * np.ones(x.shape)
        V = lambda x, y: -20*x

        # t_cfl = (1 / dx + 1 / dy)**(-1)
        # self.dt = t_cfl * percent_t_cfl
        self.dt = np.sqrt(1 / 2)
        self.r_x, self.r_y = self.dt / dx, self.dt / dy
        self.times = np.arange(0, num) * self.dt
        self.k_u, self.k_v = self.calc_pre_factors(m, V, (dx, dy))

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

    def calc_pre_factors(self, m, V, delta):
        ihc = 1j
        shape = self.spinor.shape
        x, y = Spinor.get_meshgrid(shape, delta)
        u_grid = UComponent.stag_to_reg(np.arange(self.spinor.u.num),
                                        shape[1])
        v_grid = VComponent.stag_to_reg(np.arange(self.spinor.v.num),
                                        shape[1])

        temp = ((m(x, y) + V(x, y)) / ihc).flatten()[u_grid]
        k_u = [1 + temp * self.dt / 2, (1 - temp * self.dt / 2)**(-1)]

        temp = ((V(x, y) - m(x, y)) / ihc).flatten()[v_grid]
        k_v = [1 + temp * self.dt / 2, (1 - temp * self.dt / 2)**(-1)]

        return k_u, k_v
