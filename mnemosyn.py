import os.path
import sys

from common import QtCore, QtGui, SIGNAL, Qt
from common import local_path, read_json, write_json
from newtaskdialog import NewTaskDialog
from taskwidget import TaskWidget
from tagwidget import TagWidget

class ListWidget(QtGui.QScrollArea):
    class ListWidgetContainer(QtGui.QWidget): pass

    def __init__(self):
        super().__init__()
        container = self.ListWidgetContainer()
        self.internal_layout = QtGui.QVBoxLayout(container)
        self.setWidget(container)
        self.setWidgetResizable(True)

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


class MainWindow(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mnemosyn')
        self.new_task_dialog = NewTaskDialog(self)

        main_layout = QtGui.QHBoxLayout(self)

        self.taglist, self.tasklist, self.counter \
            = read_tasklist(local_path('tasklist.json'))

        splitter = QtGui.QSplitter(self)
        main_layout.addWidget(splitter)

        # ====== Tag widget =========
        self.tag_widget = ListWidget()
        self.tag_widget.add_widgets(sorted(self.taglist), TagWidget)
        # ===========================

        # ====== Task widget ========
        self.task_widget = ListWidget()
        self.task_widget.add_widgets(self.tasklist, TaskWidget)
        # ===========================

        splitter.addWidget(self.tag_widget)
        splitter.addWidget(self.task_widget)

        def reload_css():
            with open(local_path('qtstylesheet.css'), encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        reload_css()

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, reload_css)

        def save_tasks():
            write_tasklist(local_path('tasklist.json'), self.taglist, self.tasklist)

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
            self.task_widget.append_widget(TaskWidget(data))
            self.counter += 1
            new_tags = data['tags'] - self.taglist
            self.taglist.update(data['tags'])
            for t in sorted(new_tags):
                widget = TagWidget(t)
                self.tag_widget.insert_widget(widget,
                                              sorted(self.taglist).index(t))


def read_tasklist(path):
    if not os.path.isfile(path):
        return set(), [], 1
    data = read_json(path)
    num = max([t['num'] for t in data['tasks'] ]) + 1
    return set(data['tags']), data['tasks'], num

def write_tasklist(path, taglist, tasklist):
    write_json(path, {'tags': list(taglist), 'tasks': tasklist})


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.setActiveWindow(window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

