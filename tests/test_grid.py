import unittest

import numpy as np
from numpy.testing import assert_equal

from dirac.library.grid import Grid


class TestGrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.N = 5
        cls.data = np.reshape(range(cls.N * cls.N), (cls.N, cls.N))

    def setUp(self):
        self.grid = Grid(TestGrid.data)

    def test_init(self):
        self.assertEqual(self.grid.N, TestGrid.N)
        self.assertAlmostEqual(self.grid.ds * (self.grid.N - 1), 4)
        assert_equal(self.grid.data.shape, (TestGrid.N, TestGrid.N))
        x, y = self.grid.get_space_points()
        self.assertEqual(x[0], -1)
        self.assertEqual(y[-1], 1)
        assert_equal(self.grid.data, TestGrid.data)

    def test_arithmetic(self):
        should = TestGrid.data + TestGrid.data
        is_ = self.grid + self.grid
        assert_equal(is_.data, should)

        should = TestGrid.data - TestGrid.data
        is_ = self.grid - self.grid
        assert_equal(is_.data, should)

        should = TestGrid.data + 5
        is_ = self.grid + 5
        assert_equal(is_.data, should)

        should = TestGrid.data * TestGrid.data
        is_ = self.grid * self.grid
        assert_equal(is_.data, should)

        should = TestGrid.data * 5
        is_ = self.grid * 5
        assert_equal(is_.data, should)

        assert_equal(self.grid.data, TestGrid.data)


if __name__ == '__main__':
    unittest.main()
