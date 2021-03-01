from copy import deepcopy

import time
import numpy as np

from dirac.library.spinor import *
from dirac.library.misc import *


class DiracSolver:

    def __init__(self, s0, m, V, num, pml, dt=1, c=1):
        self.spinor = s0
        self.c = c
        self.do = self.calc_dt_cfl() * dt * self.c
        self.r = self.do / self.spinor.ds
        self.times = np.arange(0, num) * self.do
        self.f_u, self.f_v = self.calc_pre_factors(m, V, pml)

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
        pass

    def advance_u(self):
        pass

    def calc_pre_factors(self, m, V, pml):
        ihc = 1j * self.c
        x, y = get_mesh(self.spinor.num)

        V_plus = (m(x) + V(x)) / ihc
        V_minus = (V(x) - m(x)) / ihc

        if pml is not None:
            V_plus -= (pml[0](x) + pml[1](y))
            V_minus -= (pml[0](x) + pml[1](y))

        f_u = [1 + V_plus * self.do / 2, (1 - V_plus * self.do / 2)**(-1)]
        f_v = [1 + V_minus * self.do / 2, (1 - V_minus * self.do / 2)**(-1)]

        return f_u, f_v
