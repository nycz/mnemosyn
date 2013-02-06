from PyQt4 import QtGui

from common import kill_theming

class TaskWidget(QtGui.QFrame):
    def __init__(self, task):
        super().__init__()
        self.task = task

        if task['closed']:
            self.hide()

        main_layout = QtGui.QVBoxLayout(self)
        kill_theming(main_layout)

        self.num = None
        self.text = None
        self.date = None
        self.desc = None

        self.create_number_and_name_row(task, main_layout)
        self.create_date_row(task, main_layout)
        self.create_tag_row(task, main_layout)
        if task['desc']:
            self.create_description_row(task, main_layout)


# ======================== UI CREATION ===================================

    def create_number_and_name_row(self, task, parent_layout):
        class TaskNumber(QtGui.QLabel): pass
        self.num = TaskNumber('#{}'.format(task['num']))

        class TaskText(QtGui.QLabel): pass
        self.text = TaskText(task['text'])

        num_text_layout = QtGui.QHBoxLayout()
        num_text_layout.addWidget(self.num)
        num_text_layout.addWidget(self.text)
        if task['desc']:
            class TaskDescriptionIndicator(QtGui.QLabel): pass
            self.desc_indicator = TaskDescriptionIndicator('[…]')
            num_text_layout.addWidget(self.desc_indicator)
        num_text_layout.addStretch()
        parent_layout.addLayout(num_text_layout)

    def create_date_row(self, task, parent_layout):
        class TaskDate(QtGui.QLabel): pass
        self.date = TaskDate(task['date'])
        if not task['date']:
            self.date.hide()
        parent_layout.addWidget(self.date)

    def create_tag_row(self, task, parent_layout):
        class TaskTag(QtGui.QLabel): pass
        class TaskTagWarning(TaskTag): pass
        tag_layout = QtGui.QHBoxLayout()
        tag_layout.setMargin(0)
        tag_layout.setSpacing(0)
        for t in sorted(task['tags']):
            tag_layout.addWidget(TaskTag(t))
        if not task['tags']:
            tag_layout.addWidget(TaskTagWarning("not tagged"))
        tag_layout.addStretch()
        parent_layout.addLayout(tag_layout)

    def create_description_row(self, task, parent_layout):
        class TaskDescription(QtGui.QLabel): pass
        self.desc = TaskDescription(task['desc'])
        self.desc.hide()
        parent_layout.addWidget(self.desc)

# ===========================================================================

    def mouseReleaseEvent(self, event):
        if self.desc:
            self.desc.setVisible(not self.desc.isVisible())
            self.desc_indicator.setVisible(not self.desc.isVisible())
