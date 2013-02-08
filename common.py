from calendar import monthrange
from datetime import date, timedelta
import json
import os.path
import re
import sys

def read_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        data = f.read()
    if not data:
        return None
    else:
        return json.loads(data)

def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))

def local_path(path):
    return os.path.join(sys.path[0], path)

def kill_theming(layout):
    layout.setMargin(0)
    layout.setSpacing(0)

def _parse_relative_date(text, start):
    if not re.match(r'\+{,3}[0-9]+', text):
        raise ValueError

    # Relative years
    if text.startswith('+++'):
        newyear = start.year + int(text[3:])
        newday = min(start.day, monthrange(newyear, start.month)[1])
        return start.replace(year=newyear, day=newday)

    # Relative months
    if text.startswith('++'):
        months = int(text[2:])
        newyear = start.year + months // 12
        newmonth = start.month + months % 12
        newday = min(start.day, monthrange(newyear, newmonth)[1])
        return date(newyear, newmonth, newday)

    # Relative days
    if text.startswith('+'):
        days = int(text[1:])
        return start + timedelta(days)

def parse_date(text, today, start=None):
    if not start:
        start = today
    if text.startswith('+'):
        return _parse_relative_date(text, start)

    if not text.isdigit():
        raise ValueError('Input is not a number.')
    if len(text) > 8:
        raise ValueError('Input is too long.')

    if len(text) <= 2:
        return today.replace(day=int(text))
    if len(text) <= 4:
        return today.replace(day=int(text[-2:]), month=int(text[-4:-2]))
    if len(text) <= 8:
        newyear = str(today.year)[:4-len(text[-8:-4])] + text[-8:-4]
        return today.replace(day=int(text[-2:]),
                             month=int(text[-4:-2]),
                             year=int(newyear))

def get_date_interval(text):
    if text.count(':') > 2:
        raise ValueError('Too many colons.')
    today = date.today()
    dates = [t.strip() for t in text.split(':')]

    if not dates[0] and len(dates) == 2:
        first_date = today
    else:
        first_date = parse_date(dates[0], today)

    if len(dates) == 2:
        second_date = parse_date(dates[1], today, first_date)
        return first_date, second_date
    else:
        return first_date, None
