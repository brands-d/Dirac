from abc import ABCMeta, abstractmethod

import numpy as np

from dirac.library.grid import *


class SpinorComponent(BaseGrid, metaclass=ABCMeta):

    def __init__(self, data, periodic=False):
        M, N = data.shape
        BaseGrid.__init__(self, N, M, periodic)

        idx = self.stag_to_reg(np.arange(self.num))
        self.data = data.flatten()[idx]

    def complex_interpolate(self, idx):
        n = self[self.get_neighbours(idx)]
        real = np.sum(np.real(n), axis=0) / 4
        imag = np.sum(np.imag(n), axis=0) / 4

        return real + 1j * imag

    def to_full_grid(self):
        full_data = np.zeros(self.M * self.N, dtype=np.complex_)
        exist_idx = self.stag_to_reg(np.arange(self.num))
        not_exist_idx = np.setdiff1d(np.arange(self.N * self.M), exist_idx)

        full_data[exist_idx] = self.data
        full_data[not_exist_idx] = self.complex_interpolate(not_exist_idx)

        return full_data.reshape(self.M, self.N)


class UComponent(UGrid, SpinorComponent):
    pass


class VComponent(VGrid, SpinorComponent):
    pass
