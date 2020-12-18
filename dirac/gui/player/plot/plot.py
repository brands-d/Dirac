import numpy as np

from pyqtgraph.opengl import (GLViewWidget, GLGridItem,
                              GLSurfacePlotItem)

from PyQt5.QtWidgets import QSizePolicy


class SurfacePlot(GLViewWidget):

    def __init__(self, *args, **kwargs):
        super(SurfacePlot, self).__init__(*args, **kwargs)

        self.image = None
        self.grid = None

        self.setup()
        self.show()

        self.toggle_grid()

    def plot(self, s):
        if self.image is not None:
            self.removeItem(self.image)

        x = np.linspace(-1, 1, s.shape[1], endpoint=True)
        y = np.linspace(-1, 1, s.shape[0], endpoint=True)
        self.image = GLSurfacePlotItem(x=x, y=y, z=abs(s),
                                       shader='heightColor',
                                       smooth=False)
        self.addItem(self.image)

    def toggle_grid(self):
        if self.grid is None:
            self.grid = GLGridItem()
            self.grid.scale(2, 2, 1)
            self.grid.setDepthValue(10)
            self.addItem(self.grid)
        else:
            self.removeItem(self.grid)
            self.grid = None

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
