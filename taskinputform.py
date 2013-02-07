from datetime import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, Qt, QEvent

from common import kill_theming

class TaskInputForm(QtGui.QFrame):
    class TaskInputFormField(QtGui.QLineEdit):
        tab_pressed = pyqtSignal()
        shift_tab_pressed = pyqtSignal()
        def event(self, event):
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Tab:
                    self.tab_pressed.emit()
                    return True
                elif event.key() == Qt.Key_Backtab:
                    self.shift_tab_pressed.emit()
                    return True
            return super().event(event)

    class TaskInputFormMultiLine(QtGui.QPlainTextEdit):
        tab_pressed = pyqtSignal()
        shift_tab_pressed = pyqtSignal()
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Tab\
                        and event.modifiers() == Qt.NoModifier:
                self.tab_pressed.emit()
            elif event.key() == Qt.Key_Backtab:
                self.shift_tab_pressed.emit()
            else:
                return super().keyPressEvent(event)

    task_created = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.number = -1

        class TaskInputFormTitle(QtGui.QLabel): pass
        self.title_label = TaskInputFormTitle('Title')

        class TaskInputFormLabel(QtGui.QLabel): pass
        text_label = TaskInputFormLabel('Text:', self)
        date_label = TaskInputFormLabel('Due date:', self)
        desc_label = TaskInputFormLabel('Description:', self)
        tags_label = TaskInputFormLabel('Tags:', self)

        class TaskInputFormField(QtGui.QLineEdit): pass
        self.text_input = self.TaskInputFormField(self)
        self.date_input = self.TaskInputFormField(self)
        self.desc_input = self.TaskInputFormMultiLine(self)
        self.tags_input = self.TaskInputFormField(self)

        self.desc_input.setFixedHeight(100)
        self.desc_input.setTabStopWidth(30)

        self.text_input.shift_tab_pressed.connect(self.tags_input.setFocus)
        self.text_input.tab_pressed.connect(self.date_input.setFocus)

        self.date_input.shift_tab_pressed.connect(self.text_input.setFocus)
        self.date_input.tab_pressed.connect(self.desc_input.setFocus)

        self.desc_input.shift_tab_pressed.connect(self.date_input.setFocus)
        self.desc_input.tab_pressed.connect(self.tags_input.setFocus)

        self.tags_input.shift_tab_pressed.connect(self.desc_input.setFocus)
        self.tags_input.tab_pressed.connect(self.text_input.setFocus)

        layout = QtGui.QFormLayout(self)
        layout.setLabelAlignment(Qt.AlignRight)
        kill_theming(layout)
        layout.addWidget(self.title_label)
        layout.addRow(text_label, self.text_input)
        layout.addRow(date_label, self.date_input)
        layout.addRow(desc_label, self.desc_input)
        layout.addRow(tags_label, self.tags_input)

        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self, self.accept)
        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, self.hide)
        self.text_input.returnPressed.connect(self.accept)
        self.date_input.returnPressed.connect(self.accept)
        self.tags_input.returnPressed.connect(self.accept)

        self.hide()

    def activate(self, number):
        if self.isVisible():
            return
        self.setDisabled(False)
        self.show()
        self.text_input.setFocus()
        self.number = number
        self.title_label.setText('New task #{}'.format(number))

    def accept(self):
        if not self.text_input.text().strip():
            return
        if self.date_input.text().strip():
            try:
                datetime.strptime(self.date_input.text().strip(), '%y%m%d%H%M')
            except ValueError:
                return
        self.hide()
        tags = set([x.strip() for x in self.tags_input.text().split(',')
                        if x.strip()])
        self.task_created.emit({
            'text': self.text_input.text(),
            'date': self.date_input.text(),
            'num': self.number,
            'tags': tags,
            'closed': False,
            'desc': self.desc_input.toPlainText()
        })
        self.text_input.setText('')
        self.date_input.setText('')
        self.desc_input.setPlainText('')
        self.tags_input.setText('')

    def hide(self):
        super().hide()
        self.setDisabled(True)
