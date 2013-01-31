from common import QtCore, QtGui, SIGNAL, Qt


class TaskWidget(QtGui.QFrame):
    def __init__(self, task):
        super().__init__()
        self.task = task

        self.mouse_down = False
        self.mouse_pos = None

        main_layout = QtGui.QVBoxLayout(self)

        top_layout = QtGui.QHBoxLayout()
        class TaskNumber(QtGui.QLabel): pass
        num = TaskNumber('#{}'.format(task['num']))
        top_layout.addWidget(num)

        class TaskText(QtGui.QLabel): pass
        self.text = TaskText(task['text'])
        top_layout.addWidget(self.text)
        top_layout.addStretch()

        btm_layout = QtGui.QHBoxLayout()
        btm_layout.addSpacing(40)
        class TaskTags(QtGui.QLabel): pass
        tags = TaskTags(', '.join(task['tags']))
        btm_layout.addWidget(tags)

        if task['closed']:
            self.setVisible(False)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(btm_layout)

        class TaskDescription(QtGui.QLabel): pass
        if task['desc']:
            self.desc = TaskDescription(task['desc'])
            self.desc.setVisible(False)
            main_layout.addWidget(self.desc)
        else:
            self.desc = None

    def mousePressEvent(self, event):
        if self.desc:
            self.mouse_pos = event.pos()
            self.mouse_down = True

    def mouseReleaseEvent(self, event):
        if self.mouse_down and self.mouse_pos == event.pos():
            self.desc.setVisible((self.desc.isVisible()+1)%2)
