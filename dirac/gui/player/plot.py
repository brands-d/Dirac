import numpy as np

from pyqtgraph import ImageView, PlotItem
from pyqtgraph.opengl import (GLViewWidget, GLGridItem,
                              GLSurfacePlotItem)

from PyQt5.QtWidgets import QSizePolicy, QWidget


class SurfacePlot(GLViewWidget):

    def __init__(self, layout, *args, **kwargs):
        self.plot_view = PlotItem()

        super(SurfacePlot, self).__init__(*args, **kwargs)
        layout.insertWidget(0, self)

        self.image = None

        self.setup()
        self.show()

    def plot(self, s, *args):
        self.image.setData(z=s)

    def get_plot_item(self):
        return self.image

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image = GLSurfacePlotItem(smooth=True,
                                       computeNormals=False, drawEdges=False,
                                       shader='heightColor', drawFaces=True)
        self.addItem(self.image)


class ImagePlot(ImageView):

    def __init__(self, layout, *args, **kwargs):
        self.plot_view = PlotItem(lockAspect=1)

        super(ImagePlot, self).__init__(*args, view=self.plot_view, **kwargs)

        layout.insertWidget(0, self)

        self.setup()
        self.show()

    def get_plot_item(self):
        return self.plot_view

    def plot(self, s):
        self.clear()
        scale = (2 / s.shape[1], 2 / s.shape[0])
        self.setImage(s.T, autoLevels=False, autoRange=True,
                      pos=(-1, -1), scale=scale)
        self.view.setRange(xRange=(-1, 1), yRange=(-1, 1))

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setRange(xRange=(-1, 1), yRange=(-1, 1))
        self.view.invertY(True)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
