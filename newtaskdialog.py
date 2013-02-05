from common import QtCore, QtGui, SIGNAL, Qt

class NewTaskDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.number = -1 # Must be set in reset()
        self.setWindowTitle('New task')
        self.setModal(True)

        layout = QtGui.QFormLayout(self)
        self.text_input = QtGui.QLineEdit(self)
        self.desc_input = QtGui.QPlainTextEdit(self)
        self.tags_input = QtGui.QLineEdit(self)

        self.title_lbl = QtGui.QLabel()
        layout.addWidget(self.title_lbl)
        layout.addRow('&Text:', self.text_input)
        layout.addRow('&Description:', self.desc_input)
        layout.addRow('&Tags:', self.tags_input)

        button_row = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save \
                                            | QtGui.QDialogButtonBox.Cancel)
        button_row.accepted.connect(self.accept)
        button_row.rejected.connect(self.reject)
        layout.addRow(button_row)

        def next_input():
            self.tags_input.setFocus()
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self, next_input)

    def reset(self, number):
        self.text_input.clear()
        self.desc_input.clear()
        self.tags_input.clear()
        self.text_input.setFocus()
        self.number = number
        self.title_lbl.setText('New task #{}'.format(number))


    def get_data(self):
        tags = [x.strip() for x in self.tags_input.text().split(',')
                if x.strip()]
        return {'text': self.text_input.text(),
                'num': self.number,
                'tags': tags,
                'closed': False,
                'desc': self.desc_input.toPlainText()}
