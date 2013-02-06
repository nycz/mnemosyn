from PyQt4 import QtGui

from common import kill_theming


class TagWidget(QtGui.QPushButton):
    class TagName(QtGui.QPushButton):
        def __init__(self, text, parent):
            super().__init__(text)
            self.parent = parent
            self.setFlat(True)
            self.setCheckable(True)

        def mousePressEvent(self, arg):
            self.parent.mousePressEvent(arg)
        def mouseReleaseEvent(self, arg):
            self.parent.mouseReleaseEvent(arg)

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.setFlat(True)
        self.setCheckable(True)

        main_layout = QtGui.QHBoxLayout(self)
        self.name_lbl = self.TagName(name, self)
        main_layout.addWidget(self.name_lbl)
        main_layout.addStretch()

        class TagTotalCount(self.TagName): pass
        self.total_count_lbl = TagTotalCount('1', self)
        main_layout.addWidget(self.total_count_lbl)

        class TagCount(self.TagName): pass
        self.count_lbl = TagCount('1', self)
        main_layout.addWidget(self.count_lbl)

        kill_theming(main_layout)
        self.setLayout(main_layout)

        def toggle_children():
            for i in (self.name_lbl, self.count_lbl, self.total_count_lbl):
                i.setChecked(self.isChecked())
        self.toggled.connect(toggle_children)

    def update_count(self, task_list_items):
        num = sum([1 for t in task_list_items
                        if self.name in t.task['tags']])
        visible = sum([1 for t in task_list_items
                        if self.name in t.task['tags']
                        and t.is_visible])
        if visible >= num:
            self.total_count_lbl.hide()
        else:
            self.total_count_lbl.show()
        self.total_count_lbl.setText('({})'.format(num))
        self.count_lbl.setText(str(visible))
