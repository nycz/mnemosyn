import calendar

from PyQt4 import QtGui

from common import kill_theming

class DateIntervalWidget(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        class DateIntervalLabel(QtGui.QLabel): pass
        class DateIntervalDummyLabel(QtGui.QLabel): pass

        layout = QtGui.QHBoxLayout(self)
        kill_theming(layout)
        self.date_label = DateIntervalLabel()

        layout.addStretch()
        layout.addWidget(self.date_label)
        layout.addStretch()
        self.hide()

    def set_interval(self, date1, date2):
        date_to_text = lambda d: '{} {} {}'.format(d.day,
                            calendar.month_name[d.month],d.year)
        text = date_to_text(date1)
        if date2:
            text += ' to ' + date_to_text(date2)
        self.date_label.setText(text)
        self.show()
