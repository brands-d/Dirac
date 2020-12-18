import unittest
from pathlib import Path

import numpy as np
from numpy.testing import assert_equal, assert_almost_equal

from dirac.model.spinor import UComponent


class TestGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = np.loadtxt(Path(__file__).parent / 'input/data.txt').view(
            complex)

    def setUp(self):
        self.u = UComponent.init_on_full_grid(TestGet.data)

    def test_get(self):
        points = np.array([[4, 23], [0, np.nan]])
        expect = np.loadtxt(Path(__file__).parent /
                            'output/data_3_23_0_12.txt').view(complex)
        assert_equal(self.u[points], expect)

    def test_complex_interpolate(self):
        assert_almost_equal(self.u.complex_interpolate([10]), 11.25 + 12.5j)


class TestArithmetic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = np.loadtxt(Path(__file__).parent / 'input/data.txt').view(
            complex)

    def setUp(self):
        self.u = UComponent.init_on_full_grid(TestArithmetic.data)

    def test_add(self):
        assert_equal((self.u + self.u).data, 2 * self.u.data)

    def test_mul(self):
        assert_equal((self.u * 2).data, 2 * self.u.data)
        assert_equal((2 * self.u).data, 2 * self.u.data)


if __name__ == '__main__':
    unittest.main()
