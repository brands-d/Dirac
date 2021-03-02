from copy import deepcopy

import time
import numpy as np

from dirac.library.spinor import *
from dirac.library.misc import *


class DiracSolver:

    def __init__(self, s0, m, V, num, abc, dt=1, c=1):
        self.spinor = s0
        self.c = c
        self.do = self.calc_dt_cfl() * dt * self.c
        self.r = self.do / self.spinor.ds
        self.times = np.arange(0, num) * self.do
        self.f_u, self.f_v = self.calc_pre_factors(m, V, abc)

    def calc_dt_cfl(self):
        return self.spinor.ds / (2 * self.c)

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

    def advance_v(self):
        u, v = self.spinor.u, self.spinor.v
        dy = self.r * (u.roll(1, -1) - u.roll(1, 1))
        dx = self.r * (u.roll(0, -1) - u.roll(0, 1))
        self.spinor.v = (v * self.f_v[0] - dy + 1j * dx) * self.f_v[1]

    def advance_u(self):
        u, v = self.spinor.u, self.spinor.v
        dy = self.r * (v.roll(1, -1) - v.roll(1, 1))
        dx = self.r * (v.roll(0, -1) - v.roll(0, 1))
        self.spinor.u = (u * self.f_u[0] - dy - 1j * dx) * self.f_u[1]

    def calc_pre_factors(self, m, V, abc):
        ihc = 1j * self.c
        x, y = get_mesh(self.spinor.N)

        V_plus = (m(x) + V(x)) / ihc
        V_minus = (V(x) - m(x)) / ihc

        if abc is not None:
            V_plus -= (abc(x) + abc(y))
            V_minus -= (abc(x) + abc(y))

        f_u = [1 + V_plus * self.do / 2, (1 - V_plus * self.do / 2)**(-1)]
        f_v = [1 + V_minus * self.do / 2, (1 - V_minus * self.do / 2)**(-1)]

        return f_u, f_v
