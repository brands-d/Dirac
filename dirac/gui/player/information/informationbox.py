import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class Information(QWidget, UI):

    def __init__(self):
        super(Information, self).__init__()
        self.setupUi(self)

        self.connect()

    def set_current_idx(self, idx, max_):
        text = '{0:.0f} / {1:.0f}'.format(idx, max_)
        self.idx_label.setText(text)

    def set_current_time(self, time):
        text = '{0:.3f} a.u.'.format(time)
        self.time_label.setText(text)

    def connect(self):
        pass
