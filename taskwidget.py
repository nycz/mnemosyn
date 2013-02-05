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

        # ====== First row ========
        class TaskNumber(QtGui.QLabel): pass
        num = TaskNumber('#{}'.format(task['num']))

        class TaskText(QtGui.QLabel): pass
        self.text = TaskText(task['text'])

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(num)
        top_layout.addWidget(self.text)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        # =========================

        # ====== Second row =======
        class TaskTags(QtGui.QLabel): pass
        tags = TaskTags(', '.join(sorted(task['tags'])))

        btm_layout = QtGui.QHBoxLayout()
        btm_layout.addSpacing(40)
        btm_layout.addWidget(tags)
        main_layout.addLayout(btm_layout)
        # =========================

        # ====== Bottom row =======
        if task['desc']:
            class TaskDescription(QtGui.QLabel): pass
            self.desc = TaskDescription(task['desc'])
            self.desc.setVisible(False)
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
            self.desc.setVisible((self.desc.isVisible()+1)%2)
