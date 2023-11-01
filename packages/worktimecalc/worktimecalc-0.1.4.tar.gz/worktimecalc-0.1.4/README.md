# Work Time Calculator
Small tool to calculate the exact business time between two datetimes.

I wasn't happy with the existing tools for their performance, while others only counted the business days. This was built with the goal of being as efficient as possible, easy to use and flexible.

## Features
- Fast! Calculations done in constant time
- Multiple ways to define working hours
- Specific schedule for each day of the week
- Can consider holidays

## Install
```
pip install worktimecalc
```

## Quick example
Just create a calculator and call it to get the difference:
```python
from worktimecalc.calc import WorkTimeCalculator

calc = WorkTimeCalculator(9, 18, 'mon tue thu fri sat')
delta = calc("2050-02-10T10:30:00", "2050-03-10T18:15:00")

print(delta.seconds)    # 675000.0
print(delta.as_dhms)    # {'days': 7, 'hours': 19, 'minutes': 30, 'seconds': 0}
print(delta.as_hms)     # {'hours': 187, 'minutes': 30, 'seconds': 0}
```

## Holidays
Pass it a list of `datetime.date` objects:
```python
holidays = [(2023, 1, 1), (2023, 5, 1), (2023, 11, 1), (2023, 12, 25)]
holidays = [datetime.date(*d) for d in CHILE_HOLIDAYS]
calc = WorkTimeCalculator(10, 18, holidays=holidays)
```

## Constructor examples
```python
calc = WorkTimeCalculator(8, 15)
calc = WorkTimeCalculator(8, 15, '1100100')
calc = WorkTimeCalculator(8, 15, 'sat tue thu mon sun')
calc = WorkTimeCalculator("08:30", "18:30")
calc = WorkTimeCalculator(9, "17:45")
calc = WorkTimeCalculator(datetime.time(8, 30), datetime.time(18, 30))
calc = WorkTimeCalculator(detail=[(8, 16), (8, 16), (8, 16), (8, 16), (8, 10), None, None])
calc = WorkTimeCalculator(detail=[(8, "16:30"), ("17:15", 20), None, None, None, None, None])
```
When in doubt simply check the descriptions for each argument.

## To do
- Overnight shifts (spanning two days)
- Small performance improvements (minmaxing)
- Allow passing holidays as list of tuples
