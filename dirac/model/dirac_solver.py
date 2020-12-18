from copy import deepcopy
import time
import numpy as np


class DiracSolver:

    def __init__(self, s0, num, delta=(0.1, 1, 1)):
        self.spinor = s0
        dt, dx, dy = delta

        self.n_u = s0.u.get_all_neighbours()
        self.n_v = s0.u.get_all_neighbours()

        m = lambda t, x, y: 1
        V = lambda t, x, y: 10
        self.k_u, self.k_v = DiracSolver.calc_pre_factors(m, V, s0.shape)

        t_cfl = (1 / dx + 1 / dy)**(-1)
        self.dt = t_cfl * dt
        self.dt = np.sqrt(1 / 2)
        self.r_x, self.r_y = self.dt / dx, self.dt / dy
        self.times = np.arange(0, num) * self.dt

    def solve(self, callback=None):
        results = []

        for i, t in enumerate(self.times):
            if callback is not None:
                is_stop = callback(i / len(self.times))
                if is_stop:
                    break

            results.append([t, deepcopy(self.spinor)])
            self.advance_u(t)
            self.advance_v(t)

        return results

    def advance_u(self, t):
        top, bottom, left, right = self.n_u

        self.spinor.u *= 1 + self.k_u(t) * self.dt / 2
        self.spinor.u -= self.r_x * (self.spinor.v[right]
                                     - self.spinor.v[left])
        self.spinor.u -= 1j * self.r_y * (self.spinor.v[top]
                                          - self.spinor.v[bottom])
        self.spinor.u *= (1 - self.k_u(t) * self.dt / 2)**(-1)

    def advance_v(self, t):
        top, bottom, left, right = self.n_v

        self.spinor.v *= 1 + self.k_v(t) * self.dt / 2
        self.spinor.v -= self.r_x * (self.spinor.u[right]
                                     - self.spinor.u[left])
        self.spinor.v += 1j * self.r_y * (self.spinor.u[top]
                                          - self.spinor.u[bottom])
        self.spinor.v *= (1 - self.k_v(t) * self.dt / 2)**(-1)

    @staticmethod
    def calc_pre_factors(m, V, shape):
        ihc = 1j
        M, N = shape
        x, y = np.meshgrid(np.linspace(-1, 1, N), np.linspace(1, -1, M))

        k_u = lambda t: (m(t, x, y) + V(t, x, y)) / ihc
        k_v = lambda t: (V(t, x, y) - m(t, x, y)) / ihc

        return k_u, k_v
