import numpy as np


def get_mesh(N):
    y = np.linspace(-1, 1, N, endpoint=True)
    x = np.reshape(y, (N, 1))

    return x, y
