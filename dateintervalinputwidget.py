from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

from common import kill_theming

class DateIntervalInputWidget(QtGui.QFrame):
    interval_entered = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        class DateIntervalInputField(QtGui.QLineEdit): pass
        class DateIntervalInputLabel(QtGui.QLabel): pass

        layout = QtGui.QVBoxLayout(self)
        kill_theming(layout)
        self.interval_input = DateIntervalInputField()

        layout.addWidget(DateIntervalInputLabel('Date interval:'))
        layout.addWidget(self.interval_input)

        self.interval_input.returnPressed.connect(self.enter)

    def enter(self):
        self.interval_entered.emit(self.interval_input.text().strip())
        self.interval_input.clear()
