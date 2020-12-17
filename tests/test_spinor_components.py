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
        self.u = UComponent(TestGet.data)

    def test_get(self):
        points = np.array([[4, 23], [0, np.nan]])
        expect = np.loadtxt(Path(__file__).parent /
                            'output/data_3_23_0_12.txt').view(complex)
        assert_equal(self.u[points], expect)

    def test_complex_interpolate(self):
        assert_almost_equal(self.u.complex_interpolate([10]), 11.25 + 12.5j)


if __name__ == '__main__':
    unittest.main()
