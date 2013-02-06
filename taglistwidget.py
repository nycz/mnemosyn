from PyQt4 import QtGui

from common import kill_theming
from genericlistwidget import ListWidget


class TagListWidget(ListWidget):

    def add_widgets(self, datalist, widget_constructor, tasklist):
        super().add_widgets(datalist, widget_constructor)
        self.update_tag_count(tasklist)
        self.btn_group = QtGui.QButtonGroup()

    def update_tag_count(self, tasklist):
        for i in range(self.internal_layout.count()):
            item = self.internal_layout.itemAt(i)
            if not item.isEmpty():
                item.widget().update_count(tasklist)
