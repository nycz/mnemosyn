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


class TagListWidget(ListWidget):

    def add_widgets(self, datalist, widget_constructor, tasklist):
        super().add_widgets(datalist, widget_constructor)
        self.update_tag_count(tasklist)

    def update_tag_count(self, tasklist):
        for i in range(self.internal_layout.count()):
            item = self.internal_layout.itemAt(i)
            if not item.isEmpty():
                item.widget().update_count(tasklist)

class TaskListWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.list_widget = ListWidget()
        layout = QtGui.QHBoxLayout(self)
        kill_theming(layout)
        layout.addWidget(self.list_widget)

    def add_widget(self, *args):
        self.list_widget.add_widget(*args)

    def add_widgets(self, *args):
        self.list_widget.add_widgets(*args)

    def append_widget(self, *args):
        self.list_widget.append_widget(*args)

    def insert_widget(self, *args):
        self.list_widget.insert_widget(*args)
