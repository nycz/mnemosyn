from PyQt4 import QtGui

from common import kill_theming
from genericlistwidget import ListWidget


class TaskListWidget(ListWidget):
    class TaskListBackground(QtGui.QFrame): pass
    def __init__(self):
        super().__init__(self.TaskListBackground)
        self.create_sort_buttons(self.main_layout)

    def create_sort_buttons(self, parent_layout):
        class SortButtonContainer(QtGui.QFrame): pass
        btn_container = SortButtonContainer(self)
        btn_layout = QtGui.QHBoxLayout(btn_container)
        parent_layout.addWidget(btn_container)
        kill_theming(btn_layout)

        btn_group = QtGui.QButtonGroup(self)

        class SortButtonLabel(QtGui.QLabel): pass
        btn_layout.addWidget(SortButtonLabel('Sort by:'))

        class SortButton(QtGui.QPushButton): pass
        for num, name in enumerate(['number', 'date', 'name']):
            btn = SortButton(name)
            btn.setCheckable(True)
            btn.setChecked(num == 0) # The first should be checked
            btn.setFlat(True)
            btn_group.addButton(btn, num)
            btn_layout.addWidget(btn)
        btn_layout.addStretch()

        btn_group.buttonClicked.connect(self.sort_list)

    def sort_list(self, btn):
        if btn.text() == 'number':
            self.sort_by_number()
        if btn.text() == 'name':
            self.sort_by_name()
        if btn.text() == 'date':
            self.sort_by_date()

    def sort_by_number(self):
        self.sort_generic(lambda x:x.num.text())

    def sort_by_name(self):
        self.sort_generic(lambda x:x.text.text().lower())

    def sort_by_date(self):
        self.sort_generic(lambda x:x.date.text())
