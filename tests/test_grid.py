import unittest
from pathlib import Path

import numpy as np
from numpy.testing import assert_equal

from dirac.library.grid import UGrid, VGrid


class TestIndexConversion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.u_idx = np.loadtxt(
            Path(__file__).parent / 'input/6_by_4_u_idx.txt')

        cls.v_idx = np.loadtxt(
            Path(__file__).parent / 'input/6_by_4_v_idx.txt')

    def setUp(self):
        N, M = 6, 4
        self.u = UGrid(N, M)
        self.v = VGrid(N, M)

    def test_reg_to_stag_u(self):
        stag_idx = self.u.reg_to_stag(TestIndexConversion.u_idx)

        assert_equal(stag_idx, range(self.u.num))

    def test_reg_to_stag_v(self):
        stag_idx = self.u.reg_to_stag(TestIndexConversion.v_idx)

        assert_equal(stag_idx, range(self.v.num))

    def test_stag_to_reg_u(self):
        reg_idx = UGrid.stag_to_reg(np.arange(self.u.num), self.u.N)

        assert_equal(TestIndexConversion.u_idx, reg_idx)

    def test_stag_to_reg_v(self):
        reg_idx = VGrid.stag_to_reg(np.arange(self.v.num), self.u.N)

        assert_equal(TestIndexConversion.v_idx, reg_idx)


class TestBoundaries(unittest.TestCase):

    def setUp(self):
        N, M = 6, 4
        self.u = UGrid(N, M)

    def test_is_top(self):
        self.assertEqual(self.u.is_top(0), True)
        self.assertEqual(self.u.is_top(14), False)
        self.assertEqual(self.u.is_top(21), False)

    def test_is_bottom(self):
        self.assertEqual(self.u.is_bottom(18), True)
        self.assertEqual(self.u.is_bottom(13), False)
        self.assertEqual(self.u.is_bottom(0), False)

    def test_is_left(self):
        self.assertEqual(self.u.is_left(0), True)
        self.assertEqual(self.u.is_left(8), False)
        self.assertEqual(self.u.is_left(11), False)

    def test_is_right(self):
        self.assertEqual(self.u.is_right(5), True)
        self.assertEqual(self.u.is_right(14), False)
        self.assertEqual(self.u.is_right(18), False)


class TestNeighbours(unittest.TestCase):

    def setUp(self):
        self.N, self.M = 6, 4

    def test_top(self):
        self.u = UGrid(self.N, self.M, periodic=False)

        assert_equal(self.u.get_top_neighbour(3), np.nan)
        self.assertEqual(self.u.get_top_neighbour(14), 8)
        self.assertEqual(self.u.get_top_neighbour(23), 17)

    def test_top_periodic(self):
        self.u = UGrid(self.N, self.M, periodic=True)

        self.assertEqual(self.u.get_top_neighbour(3), 21)
        self.assertEqual(self.u.get_top_neighbour(14), 8)
        self.assertEqual(self.u.get_top_neighbour(23), 17)

    def test_bottom(self):
        self.u = UGrid(self.N, self.M, periodic=False)

        self.assertEqual(self.u.get_bottom_neighbour(3), 9)
        self.assertEqual(self.u.get_bottom_neighbour(14), 20)
        assert_equal(self.u.get_bottom_neighbour(23), np.nan)

    def test_bottom_periodic(self):
        self.u = UGrid(self.N, self.M, periodic=True)

        self.assertEqual(self.u.get_bottom_neighbour(3), 9)
        self.assertEqual(self.u.get_bottom_neighbour(14), 20)
        self.assertEqual(self.u.get_bottom_neighbour(23), 5)

    def test_left(self):
        self.u = UGrid(self.N, self.M, periodic=False)

        assert_equal(self.u.get_left_neighbour(6), np.nan)
        self.assertEqual(self.u.get_left_neighbour(15), 14)
        self.assertEqual(self.u.get_left_neighbour(23), 22)

    def test_left_periodic(self):
        self.u = UGrid(self.N, self.M, periodic=True)

        self.assertEqual(self.u.get_left_neighbour(6), 11)
        self.assertEqual(self.u.get_left_neighbour(15), 14)
        self.assertEqual(self.u.get_left_neighbour(23), 22)

    def test_right(self):
        self.u = UGrid(self.N, self.M, periodic=False)

        self.assertEqual(self.u.get_right_neighbour(6), 7)
        self.assertEqual(self.u.get_right_neighbour(15), 16)
        assert_equal(self.u.get_right_neighbour(23), np.nan)

    def test_right_periodic(self):
        self.u = UGrid(self.N, self.M, periodic=True)

        self.assertEqual(self.u.get_right_neighbour(6), 7)
        self.assertEqual(self.u.get_right_neighbour(15), 16)
        self.assertEqual(self.u.get_right_neighbour(23), 18)

    def test_neighbours(self):
        self.u = UGrid(self.N, self.M)

        expect = np.loadtxt(Path(__file__).parent /
                            'output/neighbours_3_12_21.txt')
        assert_equal(self.u.get_neighbours([3, 12, 21]), expect)


if __name__ == '__main__':
    unittest.main()
