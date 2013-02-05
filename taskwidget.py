from common import QtCore, QtGui, SIGNAL, Qt

class TaskWidget(QtGui.QFrame):
    def __init__(self, task):
        super().__init__()
        self.task = task

        if task['closed']:
            self.setVisible(False)

        self.mouse_down = False
        self.mouse_pos = None

        main_layout = QtGui.QVBoxLayout(self)

        # Let the stylesheet take care of styling, eh?
        main_layout.setMargin(0)
        main_layout.setSpacing(0)

        # ====== Number and name ========
        class TaskNumber(QtGui.QLabel): pass
        num = TaskNumber('#{}'.format(task['num']))

        class TaskText(QtGui.QLabel): pass
        self.text = TaskText(task['text'])

        num_text_layout = QtGui.QHBoxLayout()
        num_text_layout.addWidget(num)
        num_text_layout.addWidget(self.text)
        num_text_layout.addStretch()
        main_layout.addLayout(num_text_layout)
        # ===========================

        # =========== Tags ==========
        class TaskTag(QtGui.QLabel): pass
        class TaskTagWarning(TaskTag): pass
        tag_layout = QtGui.QHBoxLayout()
        tag_layout.setMargin(0)
        tag_layout.setSpacing(0)
        for t in sorted(task['tags']):
            tag_layout.addWidget(TaskTag(t))
        if not task['tags']:
            tag_layout.addWidget(TaskTagWarning("Missing tags!"))
        tag_layout.addStretch()
        main_layout.addLayout(tag_layout)
        # =========================

        # ====== Bottom row =======
        if task['desc']:
            class TaskDescription(QtGui.QLabel): pass
            self.desc = TaskDescription(task['desc'])
            self.desc.setVisible(False)
            class TaskDescriptionIndicator(QtGui.QLabel): pass
            self.desc_indicator = TaskDescriptionIndicator('[…]')
            num_text_layout.insertWidget(num_text_layout.count()-1, self.desc_indicator)
            main_layout.addWidget(self.desc)
        else:
            self.desc = None
        # =========================

    def mousePressEvent(self, event):
        if self.desc:
            self.mouse_pos = event.pos()
            self.mouse_down = True

    def mouseReleaseEvent(self, event):
        if self.mouse_down and self.mouse_pos == event.pos():
            self.desc.setVisible(not self.desc.isVisible())
            self.desc_indicator.setVisible(not self.desc.isVisible())
