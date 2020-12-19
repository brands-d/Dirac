import unittest
from pathlib import Path

import numpy as np
from numpy.testing import assert_equal, assert_almost_equal

from dirac.library.spinor import UComponent, Spinor
from dirac.model.dirac_solver import DiracSolver


class TestDiracSolver(unittest.TestCase):

    def setUp(self):
        data = np.arange(16).reshape(4, 4)
        self.s0 = Spinor(data, data, periodic=True)
        self.solver = DiracSolver(self.s0, 10, delta=(0.1, 1, 1))

    def test_factors(self):
        k_u = self.solver.k_u[0]
        assert_equal(len(k_u), len(self.s0.u.data))
        dt = self.solver.dt
        assert_equal(dt, np.sqrt(1 / 2))
        r_x = self.solver.r_x
        assert_equal(r_x, dt)

    def test_advance_u(self):
        print(self.solver.spinor.u.data)
        print(self.solver.spinor.v.data)
        self.solver.advance_u()
        self.solver.advance_v()
        print(self.solver.spinor.u.data)
        print(self.solver.spinor.v.data)


if __name__ == '__main__':
    unittest.main()
