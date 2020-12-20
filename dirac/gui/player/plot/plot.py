import numpy as np

from pyqtgraph import ImageView, PlotItem
from pyqtgraph.opengl import (GLViewWidget, GLGridItem,
                              GLSurfacePlotItem)

from PyQt5.QtWidgets import QSizePolicy, QWidget


class SurfacePlot(GLViewWidget):

    def __init__(self, layout, x, y, *args, **kwargs):
        self.plot_view = PlotItem()

        super(SurfacePlot, self).__init__(*args, **kwargs)
        layout.insertWidget(0, self)

        self.image = None

        self.setup(x, y)
        self.show()

    def plot(self, s, *args):
        self.image.setData(z=s)

    def setup(self, x, y):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image = GLSurfacePlotItem(x=y, y=x, smooth=True,
                                       computeNormals=False, drawEdges=False,
                                       shader='heightColor', drawFaces=True)
        self.addItem(self.image)


class ImagePlot(ImageView):

    def __init__(self, layout, range, *args, **kwargs):
        self.plot_view = PlotItem()

        super(ImagePlot, self).__init__(*args, view=self.plot_view,
                                        **kwargs)

        layout.insertWidget(0, self)

        self.setup(range)
        self.show()

    def plot(self, s, range):
        self.clear()
        scale = ((range[0][1] - range[0][0]) / s.shape[1],
                 (range[1][1] - range[1][0]) / s.shape[0])
        self.setImage(s.T, autoLevels=False, autoRange=True,
                      pos=(range[1][0], range[0][0]),
                      scale=scale)

    def setup(self, range):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setRange(xRange=range[0], yRange=range[1])

        self.view.invertY(True)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
