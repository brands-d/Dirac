import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class BoundarySettings(QWidget, UI):

    def __init__(self):
        super(BoundarySettings, self).__init__()
        self.setupUi(self)

    def get_settings(self):
        periodic = self.periodic_radiobutton.isChecked()
        is_pml = self.pml_checkbox.isChecked()
        x_order = self.x_order_spinbox.value()
        y_order = self.y_order_spinbox.value()
        x_thickness = self.x_thickness_spinbox.value() / 100
        y_thickness = self.y_thickness_spinbox.value() / 100
        x_factor = self.x_factor_spinbox.value()
        y_factor = self.y_factor_spinbox.value()

        return {'periodic': periodic, 'pml': is_pml,
                'x order': x_order, 'x thickness': x_thickness,
                'y order': y_order, 'y thickness': y_thickness,
                'x factor': x_factor, 'y factor': y_factor}
