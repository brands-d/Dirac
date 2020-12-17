from abc import ABCMeta, abstractmethod

import numpy as np

from dirac.library.grid import *


class SpinorComponent(BaseGrid, metaclass=ABCMeta):

    def __init__(self, data):
        N, M = data.shape
        BaseGrid.__init__(self, N, M)

        idx = self.stag_to_reg(np.arange(self.num))
        self.data = data.flatten()[idx]


class UComponent(UGrid, SpinorComponent):
    pass


class VComponent(VGrid, SpinorComponent):
    pass
