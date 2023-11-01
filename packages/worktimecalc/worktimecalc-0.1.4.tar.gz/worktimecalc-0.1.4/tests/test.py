import datetime
import pytest


CHILE_HOLIDAYS = [
    (2023, 1, 1),
    (2023, 1, 2),
    (2023, 4, 7),
    (2023, 4, 8),
    (2023, 4, 9),
    (2023, 5, 1),
    (2023, 5, 21),
    (2023, 6, 7),
    (2023, 6, 21),
    (2023, 6, 26),
    (2023, 7, 16),
    (2023, 8, 15),
    (2023, 8, 20),
    (2023, 9, 18),
    (2023, 9, 19),
    (2023, 10, 9),
    (2023, 10, 27),
    (2023, 11, 1),
    (2023, 12, 8),
    (2023, 12, 25),
]


def format_result(result):
    times = result.split()
    times = [datetime.time.fromisoformat(x) if x != 'None' else None for x in times]
    result = list(zip(*[iter(times)] * 2))
    result = [x if x != (None, None) else None for x in result]
    return result


# fmt: off
@pytest.mark.parametrize(
    'start,end,week,holidays,detail,expected', [
        (
            9, 18, 'mon tue wed sat', None, None,
            '09:00 18:00 09:00 18:00 09:00 18:00 None None None None 09:00 18:00 None None'
        ),
        (
            8, 15, None, None, None,
            '08:00 15:00 08:00 15:00 08:00 15:00 08:00 15:00 08:00 15:00 None None None None'
        ),
        (
            8, 15, '1100100', None, None,
            '08:00 15:00 08:00 15:00 None None None None 08:00 15:00 None None None None'
        ),
        (
            8, 15, 'sat tue thu mon sun', None, None,
            '08:00 15:00 08:00 15:00 None None 08:00 15:00 None None 08:00 15:00 08:00 15:00'
        ),
        (
            "08:30", "18:30", None, None, None,
            '08:30 18:30 08:30 18:30 08:30 18:30 08:30 18:30 08:30 18:30 None None None None'
        ),
        (
            9, "17:45", None, None, None,
            '09:00 17:45 09:00 17:45 09:00 17:45 09:00 17:45 09:00 17:45 None None None None'
        ),
        (
            datetime.time(9, 00), datetime.time(17, 45), None, None, None,
            '09:00 17:45 09:00 17:45 09:00 17:45 09:00 17:45 09:00 17:45 None None None None'
        ),
        (
            None, None, None, None, [(8, "16:30"), ("17:15", 20), None, None, None, None, None],
            '08:00 16:30 17:15 20:00 None None None None None None None None None None'
        ),
    ]
)
# fmt: on
def test_constructor(start, end, week, holidays, detail, expected):
    from worktimecalc.calc import WorkTimeCalculator

    expected = format_result(expected)
    kwargs = dict(start=start, end=end, week=week, holidays=holidays, detail=detail)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    wtc = WorkTimeCalculator(**kwargs)
    assert wtc.detail == expected


@pytest.mark.parametrize(
    'date1,date2,expected_hours',
    [
        ((2023, 6, 15, 14, 30, 0), (2023, 6, 22, 10, 00, 0), 45.5),
    ],
)
def test_calc(date1, date2, expected_hours):
    from worktimecalc.calc import WorkTimeCalculator

    date1 = datetime.datetime(*date1)
    date2 = datetime.datetime(*date2)

    wtc = WorkTimeCalculator(8, 18, '1111100')
    delta = wtc(date1, date2)
    assert delta.seconds == expected_hours * 3600


@pytest.mark.parametrize(
    'date1,date2,expected_hours',
    [
        ((2023, 6, 15, 14, 30, 0), (2023, 6, 22, 10, 00, 0), 35.5),
    ],
)
def test_calc_with_holidays(date1, date2, expected_hours):
    from worktimecalc.calc import WorkTimeCalculator

    date1 = datetime.datetime(*date1)
    date2 = datetime.datetime(*date2)

    holidays = [datetime.date(*d) for d in CHILE_HOLIDAYS]
    wtc = WorkTimeCalculator(8, 18, '1111100', holidays=holidays)
    delta = wtc(date1, date2)
    assert delta.seconds == expected_hours * 3600
