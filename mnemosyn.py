import os.path
import sys

from common import QtCore, QtGui, SIGNAL, Qt
from common import local_path, read_json, write_json
from newtaskdialog import NewTaskDialog
from taskwidget import TaskWidget

class MainWindow(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mnemosyn')
        main_layout = QtGui.QHBoxLayout(self)

        self.tasklist, self.counter = read_tasklist(local_path('tasklist.json'))

        class Background(QtGui.QWidget): pass
        task_container = Background()
        task_layout = QtGui.QVBoxLayout(task_container)

        for d in self.tasklist:
            t = TaskWidget(d)
            task_layout.addWidget(t)

        task_layout.addStretch()

        task_scrollarea = QtGui.QScrollArea(self)
        task_scrollarea.setWidget(task_container)
        task_scrollarea.setWidgetResizable(True)
        main_layout.addWidget(task_scrollarea)

        def reload_css():
            with open(local_path('qtstylesheet.css'), encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        reload_css()

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, reload_css)

        def new_task():
            d = NewTaskDialog(self.counter, self)
            result = d.exec_()
            if result:
                data = d.get_data()
                self.tasklist.append(data)
                self.counter += 1
                task_layout.insertWidget(task_layout.count()-1,
                                    TaskWidget(data))

        def save_tasks():
            write_tasklist(local_path('tasklist.json'), self.tasklist)

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+N"), self, new_task)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, save_tasks)

        self.show()
        self.resize(400,600)


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

