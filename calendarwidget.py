import calendar
import datetime

from PyQt4 import QtGui

from common import kill_theming

class CalendarWidget(QtGui.QFrame):
    def __init__(self):
        super().__init__()
        class CalendarDay(QtGui.QLabel): pass
        class CalendarFiller(CalendarDay): pass
        class CalendarWeekNumber(CalendarDay): pass

        firstweek = datetime.date(2013,1,1).isocalendar()[1]

        days = [[''.join(y).strip() for y in zip(row[::3], row[1::3])]
                    for row in calendar.month(2013,1).splitlines()[2:]]
        if len(days[-1]) < 7:
            days[-1].extend(['']*(7-len(days[-1])))
        if len(days) < 6:
            days.append(['']*7)
        days = [[str(weeknum)] + week for weeknum, week in zip(range(firstweek, firstweek+6), days)]

        layout = QtGui.QGridLayout(self)
        kill_theming(layout)

        item = []

        for y in range(6):
            item.append([])
            for x in range(8):
                if x == 0:
                    widget = CalendarWeekNumber
                elif days[y][x] == '':
                    widget = CalendarFiller
                else:
                    widget = CalendarDay
                item[y].append(widget(days[y][x]))
                layout.addWidget(item[y][x], y, x)
