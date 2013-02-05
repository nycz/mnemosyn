from common import QtCore, QtGui, SIGNAL, Qt


class TagWidget(QtGui.QFrame):
    def __init__(self, name):
        super().__init__()
        self.name = name

        main_layout = QtGui.QHBoxLayout(self)
        class TagName(QtGui.QLabel): pass
        main_layout.addWidget(TagName(name))
        main_layout.addStretch()
        class TagCount(QtGui.QLabel): pass
        self.count_lbl = TagCount('1')
        main_layout.addWidget(self.count_lbl)

        # Let the stylesheet take care of styling, eh?
        main_layout.setMargin(0)
        main_layout.setSpacing(0)

    def update_count(self, tasklist):
        num = sum([1 for t in tasklist if self.name in t['tags']])
        self.count_lbl.setText(str(num))
