import os.path
import sys

from PyQt4 import QtGui

from common import local_path, read_json, write_json, kill_theming
from newtaskdialog import NewTaskDialog
from taglistwidget import TagListWidget
from tasklistwidget import TaskListWidget


class MainWindow(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mnemosyn')
        self.new_task_dialog = NewTaskDialog(self)

        main_layout = QtGui.QHBoxLayout(self)
        kill_theming(main_layout)

        self.taglist, self.tasklist, self.counter \
            = read_tasklist(local_path('tasklist.json'))

        splitter = QtGui.QSplitter(self)
        main_layout.addWidget(splitter)

        # ====== Task widget ========
        self.task_list_widget = TaskListWidget()
        self.task_list_widget.add_widgets(self.tasklist)
        # ===========================

        # ====== Tag widget =========
        self.tag_list_widget = TagListWidget(self.task_list_widget.list_items)
        self.tag_list_widget.add_widgets(sorted(self.taglist))
        self.tag_list_widget.tag_selection_updated.connect(\
                        self.task_list_widget.update_tag_selection)
        # ===========================

        splitter.addWidget(self.tag_list_widget)
        splitter.addWidget(self.task_list_widget)
        splitter.setStretchFactor(0,0)
        splitter.setStretchFactor(1,1)

        def reload_css():
            with open(local_path('qtstylesheet.css'), encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        reload_css()

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, reload_css)

        def save_tasks():
            write_tasklist(local_path('tasklist.json'), self.taglist,
                            self.task_list_widget.list_items())

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+N"), self, self.new_task)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, save_tasks)

        self.show()
        self.resize(800,600)
        splitter.moveSplitter(200,1)
        self.tag_list_widget.update_tag_count()

    def new_task(self):
        self.new_task_dialog.reset(self.counter)
        result = self.new_task_dialog.exec_()
        if result:
            data = self.new_task_dialog.get_data()
            self.tasklist.append(data)
            self.task_list_widget.append_widget(data)
            self.counter += 1
            new_tags = data['tags'] - self.taglist
            self.taglist.update(data['tags'])
            for t in sorted(new_tags):
                self.tag_list_widget.insert_widget(t,
                        sorted(self.taglist).index(t))
            self.tag_list_widget.update_tag_count()


def read_tasklist(path):
    data = read_json(path)
    if data is None:
        return set(), [], 1
    num = max([t['num'] for t in data['tasks'] ]) + 1
    return set(data['tags']), data['tasks'], num

def write_tasklist(path, taglist, tasklist):
    out = []
    for x in tasklist:
        x['tags'] = list(x['tags'])
        out.append(x)
    write_json(path, {'tags': list(taglist), 'tasks': out})


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.setActiveWindow(window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

