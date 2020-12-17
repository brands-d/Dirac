from abc import ABCMeta, abstractmethod

import numpy as np


class BaseGrid(metaclass=ABCMeta):

    def __init__(self, N, M, periodic=False):
        self.N = int(N)
        self.M = int(M)
        self.periodic = periodic
        self.num = int(N * M / 2)

    @staticmethod
    def reg_to_stag(idx):
        return (idx / 2).astype(np.uint16)

    def is_top(self, idx):
        return idx < self.N

    def is_bottom(self, idx):
        return idx >= self.N * (self.M - 1)

    def is_left(self, idx):
        return idx % self.N == 0

    def is_right(self, idx):
        return (idx + 1) % self.N == 0

    def get_top_neighbour(self, idx):
        if self.is_top(idx):
            if self.periodic:
                return idx + self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx - self.N

    def get_bottom_neighbour(self, idx):
        if self.is_bottom(idx):
            if self.periodic:
                return idx - self.N * (self.M - 1)
            else:
                return np.nan
        else:
            return idx + self.N

    def get_left_neighbour(self, idx):
        if self.is_left(idx):
            if self.periodic:
                return idx + (self.N - 1)
            else:
                return np.nan
        else:
            return idx - 1

    def get_right_neighbour(self, idx):
        if self.is_right(idx):
            if self.periodic:
                return idx - (self.N - 1)
            else:
                return np.nan
        else:
            return idx + 1

    def get_neighbours(self, idx):
        neighbours = []
        for i in idx:
            temp = [self.get_top_neighbour(i),
                    self.get_bottom_neighbour(i),
                    self.get_right_neighbour(i),
                    self.get_left_neighbour(i)]
            neighbours.append(temp)

        return np.array(neighbours).T

    def __getitem__(self, idx):
        old_shape = idx.shape
        idx = idx.flatten()
        nan_mask = np.isnan(idx)
        not_nan_mask = np.invert(nan_mask)

        data = np.zeros(idx.shape, dtype=np.complex_)
        stag_idx = BaseGrid.reg_to_stag(idx[not_nan_mask])

        data[nan_mask] = np.nan
        data[not_nan_mask] = self.data[stag_idx]

        return data.reshape(old_shape)

    @abstractmethod
    def stag_to_reg(self, idx):
        pass


class UGrid(BaseGrid):

    def stag_to_reg(self, idx):
        temp = 2 * idx
        temp += (temp / self.N).astype(np.uint16) % 2
        return temp


class VGrid(BaseGrid):

    def stag_to_reg(self, idx):
        temp = 2 * idx
        temp += 1 - (temp / self.N).astype(np.uint16) % 2
        return temp
