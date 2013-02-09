from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

from common import kill_theming
from genericlistwidget import ListWidget
from tagwidget import TagWidget


class TagListWidget(ListWidget):
    class TagListBackground(QtGui.QFrame): pass

    tag_selection_updated = pyqtSignal(str, bool)

    def __init__(self, get_filterable_items):
        super().__init__(self.TagListBackground, TagWidget)
        self.btn_group = QtGui.QButtonGroup()
        self.btn_group.setExclusive(False)
        self.get_filterable_items = get_filterable_items

        def button_toggled(button):
            self.tag_selection_updated.emit(button.name, button.isChecked())
            self.update_tag_count()
        self.btn_group.buttonClicked.connect(button_toggled)

    def update_tag_count(self):
        for item in self.list_items():
            item.update_count(self.get_filterable_items())

    # ================== Overrides =====================
    def add_widgets(self, datalist):
        super().add_widgets(datalist)
        for item in self.list_items():
            self.btn_group.addButton(item)

    def append_widget(self, data):
        new_item = super().append_widget(data)
        self.btn_group.addButton(new_item)

    def insert_widget(self, data, pos):
        new_item = super().insert_widget(data, pos)
        self.btn_group.addButton(new_item)
