from abc import ABCMeta, abstractmethod

import numpy as np

from dirac.library.grid import *


class SpinorComponent(BaseGrid, metaclass=ABCMeta):

    def __init__(self, data, shape, periodic=False):
        M, N = shape
        self.data = data

        BaseGrid.__init__(self, N, M, periodic)

    @classmethod
    def init_on_full_grid(cls, data, periodic=False):
        shape = data.shape
        idx = cls.stag_to_reg(np.arange(int(data.size / 2)), shape[1])
        data = data.flatten()[idx]

        return cls(data, shape, periodic)

    def complex_interpolate(self, idx):
        n = self[self.get_neighbours(idx)]
        real = np.sum(np.real(n), axis=0) / 4
        imag = np.sum(np.imag(n), axis=0) / 4

        return real + 1j * imag

    def to_full_grid(self):
        full_data = np.zeros(self.M * self.N, dtype=np.complex_)
        exist_idx = self.stag_to_reg(np.arange(self.num), self.N)
        not_exist_idx = np.setdiff1d(np.arange(self.N * self.M), exist_idx)

        full_data[exist_idx] = self.data
        full_data[not_exist_idx] = self.complex_interpolate(not_exist_idx)

        return full_data.reshape(self.M, self.N)

    def __add__(self, other):
        if isinstance(other, type(self)):
            data = self.data + other.data
        else:
            data = self.data + other

        new = type(self)(data, (self.M, self.N), self.periodic)
        return new

    def __mul__(self, other):
        if isinstance(other, type(self)):
            data = self.data * other.data
        else:
            data = self.data * other

        new = type(self)(data, (self.M, self.N), self.periodic)
        return new

    def __rmul__(self, other):
        if isinstance(other, type(self)):
            data = self.data * other.data
        else:
            data = self.data * other

        new = type(self)(data, (self.M, self.N), self.periodic)
        return new

class UComponent(UGrid, SpinorComponent):
    pass


class VComponent(VGrid, SpinorComponent):
    pass


class Spinor:

    def __init__(self, data, periodic=False):
        self.u = UComponent(data, periodic)
        self.v = VComponent(data, periodic)
