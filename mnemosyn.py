import os.path
import sys

from common import QtCore, QtGui, SIGNAL, Qt
from common import local_path, read_json, write_json
from newtaskdialog import NewTaskDialog
from taskwidget import TaskWidget

class ListWidget(QtGui.QScrollArea):
    class ListWidgetContainer(QtGui.QWidget): pass

    def __init__(self):
        super().__init__()
        container = self.ListWidgetContainer()
        self.internal_layout = QtGui.QVBoxLayout(container)
        self.setWidget(container)
        self.setWidgetResizable(True)

    def addWidget(self, widget):
        self.internal_layout.addWidget(widget)

    def addWidgets(self, datalist, widget_constructor):
        for d in datalist:
            self.internal_layout.addWidget(widget_constructor(d))
        self.internal_layout.addStretch()

    def appendWidget(self, widget):
        self.internal_layout.insertWidget(self.internal_layout.count()-1,
                                          widget)

    def insertWidget(self, widget, pos):
        self.internal_layout.insertWidget(pos, widget)


class MainWindow(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mnemosyn')
        self.new_task_dialog = NewTaskDialog(self)

        self.tasklist, self.counter = read_tasklist(local_path('tasklist.json'))
        main_layout = QtGui.QHBoxLayout(self)


        splitter = QtGui.QSplitter(self)
        main_layout.addWidget(splitter)

        # ====== Task widget ========
        self.task_widget = ListWidget()
        self.task_widget.addWidgets(self.tasklist, TaskWidget)
        # ===========================

        splitter.addWidget(self.task_widget)

        def reload_css():
            with open(local_path('qtstylesheet.css'), encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        reload_css()

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, reload_css)

        def save_tasks():
            write_tasklist(local_path('tasklist.json'), self.tasklist)

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+N"), self, self.new_task)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, save_tasks)

        self.show()
        self.resize(800,600)

    def new_task(self):
        self.new_task_dialog.reset(self.counter)
        result = self.new_task_dialog.exec_()
        if result:
            data = self.new_task_dialog.get_data()
            self.tasklist.append(data)
            self.counter += 1
            self.task_widget.appendWidget(TaskWidget(data))


def read_tasklist(path):
    if not os.path.isfile(path):
        return [], 1

    tasklist = read_json(path)
    num = max([t['num'] for t in tasklist]) + 1

    return tasklist, num

def write_tasklist(path, data):
    write_json(path, data)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.setActiveWindow(window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

