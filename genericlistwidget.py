from PyQt4 import QtGui

from common import kill_theming


class ListWidget(QtGui.QFrame):
    def __init__(self, list_widget_background, item_constructor):
        super().__init__()
        self.internal_widget = ListWidgetScrollArea(list_widget_background)
        self.internal_widget.item_constructor = item_constructor
        self.main_layout = QtGui.QVBoxLayout(self)
        kill_theming(self.main_layout)
        self.main_layout.addWidget(self.internal_widget)

    def list_items(self):
        return self.internal_widget.list_items

    def sort_generic(self, *args):
        self.internal_widget.sort_generic(*args)

    def add_widgets(self, *args):
        self.internal_widget.add_widgets(*args)

    def append_widget(self, *args):
        return self.internal_widget.append_widget(*args)

    def insert_widget(self, *args):
        return self.internal_widget.insert_widget(*args)


class ListWidgetScrollArea(QtGui.QScrollArea):

    def __init__(self, list_widget_background):
        super().__init__()
        container = list_widget_background()
        self.list_items = []
        self.layout = QtGui.QVBoxLayout(container)
        kill_theming(self.layout)
        self.setWidget(container)
        self.setWidgetResizable(True)

    def sort_generic(self, key):
        widgets = []
        while True:
            item = self.layout.takeAt(0)
            if not item:
                break
            if not item.widget():
                continue
            widgets.append(item.widget())
        widgets.sort(key=key)
        for item in widgets:
            self.layout.addWidget(item)
        self.layout.addStretch()

    def add_widgets(self, datalist):
        for d in datalist:
            item = self.item_constructor(d)
            self.layout.addWidget(item)
            self.list_items.append(item)
        self.layout.addStretch()

    def append_widget(self, data):
        item = self.item_constructor(data)
        self.layout.insertWidget(self.layout.count()-1, item)
        self.list_items.append(item)
        return item

    def insert_widget(self, data, pos):
        item = self.item_constructor(data)
        self.layout.insertWidget(pos, item)
        self.list_items.append(item)
        return item
