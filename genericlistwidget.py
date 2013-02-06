from PyQt4 import QtGui

from common import kill_theming


class ListWidget(QtGui.QScrollArea):
    class ListWidgetContainer(QtGui.QWidget): pass

    def __init__(self):
        super().__init__()
        container = self.ListWidgetContainer()
        self.internal_layout = QtGui.QVBoxLayout(container)
        kill_theming(self.internal_layout)
        self.setWidget(container)
        self.setWidgetResizable(True)

    def sort_generic(self, key):
        widgets = []
        while True:
            item = self.internal_layout.takeAt(0)
            if not item:
                break
            if not item.widget():
                continue
            widgets.append(item.widget())
        widgets.sort(key=key)
        for item in widgets:
            self.internal_layout.addWidget(item)
        self.internal_layout.addStretch()

    def add_widget(self, widget):
        self.internal_layout.addWidget(widget)

    def add_widgets(self, datalist, widget_constructor):
        for d in datalist:
            self.internal_layout.addWidget(widget_constructor(d))
        self.internal_layout.addStretch()

    def append_widget(self, widget):
        self.internal_layout.insertWidget(self.internal_layout.count()-1,
                                          widget)

    def insert_widget(self, widget, pos):
        self.internal_layout.insertWidget(pos, widget)
