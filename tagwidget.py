from common import QtCore, QtGui, SIGNAL, Qt


class TagWidget(QtGui.QFrame):
    def __init__(self, name):
        super().__init__()

        main_layout = QtGui.QVBoxLayout(self)

        lbl = QtGui.QLabel(name)
        main_layout.addWidget(lbl)
