import numpy as np

from dirac.library.grid import Grid


class Spinor():

    def __init__(self, u, v):
        self.u = Grid(u)
        self.v = Grid(v)

    @property
    def ds(self):
        return self.u.ds

    @property
    def num(self):
        return self.u.num

    def __add__(self, other):
        if type(other) == Spinor:
            u = self.u + other.u
            v = self.v + other.v

        else:
            u = self.u + other
            v = self.v + other

        return Spinor(u, v)

    def __mul__(self, other):
        if type(other) == Spinor:
            u = self.u * other.u
            v = self.v * other.v

        else:
            u = self.u * other
            v = self.v * other

        return Spinor(u, v)

    def __sub__(self, other):
        return self + (-1) * other

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        norm = np.real(np.sqrt(self.u.abs_square() + self.v.abs_square()))
        return norm
