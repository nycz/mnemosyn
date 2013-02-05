from common import QtCore, QtGui, SIGNAL, Qt


class TagWidget(QtGui.QFrame):
    def __init__(self, name):
        super().__init__()
        self.name = name

        main_layout = QtGui.QHBoxLayout(self)
        main_layout.addWidget(QtGui.QLabel(name))
        main_layout.addStretch()
        self.count_lbl = QtGui.QLabel('1')
        main_layout.addWidget(self.count_lbl)

    def update_count(self, tasklist):
        num = sum([1 for t in tasklist if self.name in t['tags']])
        self.count_lbl.setText(str(num))
