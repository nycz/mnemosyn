from PyQt4 import QtGui

from common import kill_theming
from genericlistwidget import ListWidget


class TagListWidget(ListWidget):
    class TagListBackground(QtGui.QFrame): pass
    def __init__(self):
        super().__init__(self.TagListBackground)

    def add_widgets(self, datalist, widget_constructor, tasklist):
        super().add_widgets(datalist, widget_constructor)
        self.update_tag_count(tasklist)

    def update_tag_count(self, tasklist):
        for i in range(self.internal_widget.layout.count()):
            item = self.internal_widget.layout.itemAt(i)
            if not item.isEmpty():
                item.widget().update_count(tasklist)
