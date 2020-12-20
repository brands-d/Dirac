from abc import ABCMeta, abstractmethod

import numpy as np


class BaseGrid(metaclass=ABCMeta):

    def __init__(self, shape, range=((-1, 1), (-1, 1)), periodic=False):
        self.N = int(shape[1])
        self.M = int(shape[0])
        self.range = range
        self.dx = 2 * (range[0][1] - range[0][0]) / (self.N - 1)
        self.dy = 2 * (range[1][1] - range[1][0]) / (self.M - 1)
        self.periodic = periodic
        self.num = int(self.N * self.M / 2)

    @staticmethod
    def reg_to_stag(idx):
        return (idx / 2).astype(np.uint16)

    @staticmethod
    def get_x_axis(range, N):
        x = np.linspace(range[0][0], range[0][1], N,
                        endpoint=True)

        return x

    @staticmethod
    def get_y_axis(range, M):
        y = np.linspace(range[1][0], range[1][1], M,
                        endpoint=True)

        return y

    @classmethod
    def get_full_meshgrid(cls, range, shape):
        M, N = shape
        x = cls.get_x_axis(range, N)
        y = cls.get_y_axis(range, M)

        return np.meshgrid(y, x)

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

    def get_all_neighbours(self):
        idx = self.stag_to_reg(np.arange(self.num), self.N)
        return self.get_neighbours(idx)

    def get_space_points(self):
        idx = self.stag_to_reg(np.arange(self.num), self.N)

        X, Y = self.get_full_meshgrid(self.range, self.shape)

        x = X.flatten()[idx]
        y = Y.flatten()[idx]

        return np.array(x), np.array(y)

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

    @staticmethod
    @abstractmethod
    def stag_to_reg(idx, N):
        pass


class UGrid(BaseGrid):

    @staticmethod
    def stag_to_reg(idx, N):
        temp = 2 * idx
        temp += (temp / N).astype(np.uint16) % 2
        return temp


class VGrid(BaseGrid):

    @staticmethod
    def stag_to_reg(idx, N):
        temp = 2 * idx
        temp += 1 - (temp / N).astype(np.uint16) % 2

        return temp
