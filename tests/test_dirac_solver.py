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
        m = lambda x: np.ones(x.shape)
        V = lambda x: np.ones(x.shape)
        self.solver = DiracSolver(self.s0, m, V, 10)

    def test_factors(self):
        k_u = self.solver.f_u[0]
        assert_equal(len(k_u), len(self.s0.u.data))

    def test_advance_u(self):
        self.solver.advance_u()
        self.solver.advance_v()


if __name__ == '__main__':
    unittest.main()
