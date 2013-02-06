from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

from common import kill_theming
from genericlistwidget import ListWidget


class TagListWidget(ListWidget):
    class TagListBackground(QtGui.QFrame): pass

    tag_selection_updated = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__(self.TagListBackground)
        self.btn_group = QtGui.QButtonGroup()
        self.btn_group.setExclusive(False)

        def button_toggled(button):
            self.tag_selection_updated.emit(button.name, button.isChecked())
        self.btn_group.buttonClicked.connect(button_toggled)

    def update_tag_count(self, tasklist):
        for item in self.list_items():
            item.update_count(tasklist)

    # ================== Overrides =====================
    def add_widgets(self, datalist, widget_constructor, tasklist):
        super().add_widgets(datalist, widget_constructor)
        for item in self.list_items():
            self.btn_group.addButton(item)
        self.update_tag_count(tasklist)

    def append_widget(self, widget):
        super().append_widget(widget)
        self.btn_group.addButton(widget)

    def insert_widget(self, widget, pos):
        super().insert_widget(widget, pos)
        self.btn_group.addButton(widget)
