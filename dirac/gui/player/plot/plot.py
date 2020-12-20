import numpy as np

from pyqtgraph import ImageView, PlotItem
from pyqtgraph.opengl import (GLViewWidget, GLGridItem,
                              GLSurfacePlotItem)

from PyQt5.QtWidgets import QSizePolicy, QWidget


class SurfacePlot(GLViewWidget):

    def __init__(self, layout, shape, *args, **kwargs):
        self.plot_view = PlotItem()

        super(SurfacePlot, self).__init__(*args, **kwargs)
        layout.insertWidget(0, self)

        self.image = None

        self.setup(shape)
        self.show()

    def plot(self, s):
        self.image.setData(z=s)

    def setup(self, shape):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        x = np.linspace(-1, 1, shape[0])
        y = np.linspace(-1, 1, shape[1])
        self.image = GLSurfacePlotItem(x=x, y=y, smooth=True,
                                       computeNormals=False, drawEdges=False,
                                       shader='heightColor', drawFaces=True)
        self.addItem(self.image)


class ImagePlot(ImageView):

    def __init__(self, layout, *args, **kwargs):
        self.plot_view = PlotItem()

        super(ImagePlot, self).__init__(*args, view=self.plot_view,
                                        **kwargs)

        layout.insertWidget(0, self)

        self.setup()
        self.show()

    def plot(self, s):
        self.clear()
        self.setImage(s, autoLevels=False)

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.view.invertY(False)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
