# fmt: off
INVALID_DETAIL = (
    'Invalid detail format. Examples:\n'
    '    [(9, 17), (9, 17), (9, 17), (9, 17), (9, 17), None, None]\n'
    '    [(datetime.time(9, 30), datetime.time(17, 30), ...]\n'
    '    [("09:30", "17:30"), ("09:30", "17:30"), ...]\n]'
)

INVALID_WEEK = (
    'Invalid week format. Examples:\n'
    '    "1111100"\n'
    '    "mon tue wed thu fri"\n'
)

INVALID_START_TIME = 'Invalid start time. Must be datetime.time or int or str (ISO format).'

INVALID_END_TIME = 'Invalid end time. Must be datetime.time or int or str (ISO format).'

INVALID_HOLIDAYS = 'Invalid holidays. Must be a list of datetime.date objects.'
