from copy import deepcopy

import time
import numpy as np

from dirac.library.spinor import *


class DiracSolver:

    def __init__(self, s0, m, V, num, pml, dt=1, c=1):
        self.spinor = s0
        self.do = self.calc_dt_cfl(c) * dt * c
        self.n_u, self.n_v = s0.get_neighbours()
        self.r_x, self.r_y = self.do / s0.dx, self.do / s0.dy

        self.times = np.arange(0, num) * self.do
        self.f_u, self.f_v = self.calc_pre_factors(m, V, pml, c)

    def calc_dt_cfl(self, c):
        return 1 / (c / self.spinor.dx + c / self.spinor.dy)

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
        self.spinor.u *= self.f_u[0]
        self.spinor.u -= 1j * self.r_x * (self.spinor.v[self.n_u[2]]
                                          - self.spinor.v[self.n_u[3]])
        self.spinor.u -= self.r_y * (self.spinor.v[self.n_u[0]]
                                     - self.spinor.v[self.n_u[1]])
        self.spinor.u *= self.f_u[1]

    def advance_v(self):
        self.spinor.v *= self.f_v[0]
        self.spinor.v += 1j * self.r_x * (self.spinor.u[self.n_v[2]]
                                          - self.spinor.u[self.n_v[3]])
        self.spinor.v -= self.r_y * (self.spinor.u[self.n_v[0]]
                                     - self.spinor.u[self.n_v[1]])
        self.spinor.v *= self.f_v[1]

    def advance_half_v(self, direction=1):
        self.spinor.v *= self.f_v2[0]
        self.spinor.v += 1j * self.r_x * (self.spinor.u[self.n_v[2]]
                                          - self.spinor.u[self.n_v[3]]) / 2
        self.spinor.v -= self.r_y * (self.spinor.u[self.n_v[0]]
                                     - self.spinor.u[self.n_v[1]]) / 2
        self.spinor.v *= self.f_v2[1]

    def calc_pre_factors(self, m, V, pml, c=1):
        ihc = 1j * c
        x_u, y_u = self.spinor.u.get_space_points()
        x_v, y_v = self.spinor.v.get_space_points()

        V_plus = (m(x_u) + V(x_u)) / ihc
        V_minus = (V(x_v) - m(x_v)) / ihc

        if pml is not None:
            V_plus -= (pml[0](x_u) + pml[1](y_u))
            V_minus -= (pml[0](x_v) + pml[1](y_v))

        f_u = [1 + V_plus * self.do / 2, (1 - V_plus * self.do / 2)**(-1)]
        f_v = [1 + V_minus * self.do / 2, (1 - V_minus * self.do / 2)**(-1)]

        return f_u, f_v
