import numpy as np


class Grid():

    def __init__(self, data):
        self.N = int(data.shape[0])
        self.ds = 4 / (self.N - 1)
        self.num = int(self.N**2)
        self.data = data


    def roll(self, axis, shift):
        return np.roll(self.data, shift, axis=axis)

    def abs_square(self):
        return self.data * np.conjugate(self.data)

    def __add__(self, other):
        if type(other) == Grid:
            data = self.data + other.data

        else:
            data = self.data + other

        return Grid(data)

    def __mul__(self, other):
        if type(other) == Grid:
            data = self.data * other.data


        else:
            data = self.data * other

        return Grid(data)

    def __sub__(self, other):
        return self + (-1) * other

    def __rmul__(self, other):
        return self * other
