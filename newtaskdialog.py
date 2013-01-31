from common import QtCore, QtGui, SIGNAL, Qt

class NewTaskDialog(QtGui.QDialog):
    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.number = number
        self.setWindowTitle('New task')
        layout = QtGui.QFormLayout(self)
        self.text_input = QtGui.QLineEdit(self)
        self.desc_input = QtGui.QLineEdit(self)
        #TODO: tags

        layout.addWidget(QtGui.QLabel('New task #{}'.format(number)))
        layout.addRow('&Text:', self.text_input)
        layout.addRow('&Description:', self.desc_input)

        button_row = QtGui.QHBoxLayout()
        layout.addRow(button_row)

        ok_btn = QtGui.QPushButton('&OK')
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QtGui.QPushButton('&Cancel')
        cancel_btn.clicked.connect(self.reject)
        button_row.addStretch()
        button_row.addWidget(ok_btn)
        button_row.addSpacing(40)
        button_row.addWidget(cancel_btn)
        button_row.addStretch()

        self.setModal(True)

    def get_data(self):
        return {'text': self.text_input.text(),
                'num': self.number,
                'tags': [],
                'closed': False,
                'desc': self.desc_input.text()}
