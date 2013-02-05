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

        button_row = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save \
                                            | QtGui.QDialogButtonBox.Cancel)
        button_row.accepted.connect(self.accept)
        button_row.rejected.connect(self.reject)
        layout.addRow(button_row)


        self.setModal(True)

    def get_data(self):
        return {'text': self.text_input.text(),
                'num': self.number,
                'tags': [],
                'closed': False,
                'desc': self.desc_input.text()}
