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


class TagListWidget(ListWidget):

    def add_widgets(self, datalist, widget_constructor, tasklist):
        super().add_widgets(datalist, widget_constructor)
        self.update_tag_count(tasklist)

    def update_tag_count(self, tasklist):
        for i in range(self.internal_layout.count()):
            item = self.internal_layout.itemAt(i)
            if not item.isEmpty():
                item.widget().update_count(tasklist)


class TaskListWidget(QtGui.QFrame):

    def __init__(self):
        super().__init__()
        self.list_widget = ListWidget()
        main_layout = QtGui.QVBoxLayout(self)
        kill_theming(main_layout)
        main_layout.addWidget(self.list_widget)
        self.create_sort_buttons(main_layout)

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
        self.list_widget.sort_generic(lambda x:x.num.text())

    def sort_by_name(self):
        self.list_widget.sort_generic(lambda x:x.text.text().lower())

    def sort_by_date(self):
        self.list_widget.sort_generic(lambda x:x.date.text())


    # ============= Overrides =============== #
    def add_widget(self, *args):
        self.list_widget.add_widget(*args)

    def add_widgets(self, *args):
        self.list_widget.add_widgets(*args)

    def append_widget(self, *args):
        self.list_widget.append_widget(*args)

    def insert_widget(self, *args):
        self.list_widget.insert_widget(*args)
    # ======================================= #
