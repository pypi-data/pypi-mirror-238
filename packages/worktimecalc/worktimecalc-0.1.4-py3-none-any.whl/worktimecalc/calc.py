import datetime
from typing import Any

from worktimecalc import error_messages
from worktimecalc.delta import WorkTimeDelta


WEEKDAY_NAMES = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class WorkTimeCalculator:
    """
    Calculator object.
    """

    @staticmethod
    def __process_time(time: Any) -> datetime.time:
        if isinstance(time, int):
            time = datetime.time(time)
        elif isinstance(time, str):
            time = datetime.time.fromisoformat(time)
        elif not isinstance(time, datetime.time):
            return None
        return time

    @staticmethod
    def __process_detail(detail: list) -> bool:
        if not isinstance(detail, list):
            return None
        if len(detail) != 7:
            return None

        for day, times in enumerate(detail):
            if times is None:
                continue
            if len(times) != 2:
                return None

            times = list(times)
            for i in range(2):
                times[i] = WorkTimeCalculator.__process_time(times[i])
                if times[i] is None:
                    return None
            if times[0] >= times[1]:
                return None
            detail[day] = tuple(times)
        return detail

    @staticmethod
    def __process_week(week: str) -> list:
        if not isinstance(week, str):
            return None

        if len(week) == 7 and all(c in '01' for c in week):
            week = [bool(int(c)) for c in week]
        else:
            week = week.lower().split()
            week = [day in week for day in WEEKDAY_NAMES]
        return week

    def __init__(
        self,
        start: Any = None,
        end: Any = None,
        week: str = '1111100',
        holidays: list = None,
        detail: list = None,
    ):
        """Constructor. Builds a calculator object with the given schedule definition.

        Args:
            start (any, optional): Start time of the work day. Can be an integer (9), an ISO time string ("09:30") or a datetime.time object. Defaults to None.
            end (any, optional): End time of the work day. Can be an integer (9), an ISO time string ("09:30") or a datetime.time object. Defaults to None.
            week (str, optional): Working days of the week. Can be a string of 7 binary digits (like '1101010'), or a string with space-separated 3-letter days (like 'mon tue thu sat'). Defaults to '1111100'.
            holidays (list, optional): List of holidays. Must be a list of datetime.date objects. Defaults to None.
            detail (list, optional): Full schedule definition. Must be a list of tuples indicating start and end time (same format as start and end arguments), or None in place of the tuple to represent a non-working day. When present, start end and week arguments are ignored. Defaults to None.
        """
        if isinstance(detail, list):
            detail = WorkTimeCalculator.__process_detail(detail)
            if detail is None:
                raise ValueError(error_messages.INVALID_DETAIL)
            self.detail = detail

        else:
            week = WorkTimeCalculator.__process_week(week)
            if week is None:
                raise ValueError(error_messages.INVALID_WEEK)

            start = WorkTimeCalculator.__process_time(start)
            end = WorkTimeCalculator.__process_time(end)
            if start is None:
                raise ValueError(error_messages.INVALID_START_TIME)
            if end is None:
                raise ValueError(error_messages.INVALID_END_TIME)

            self.detail = [(start, end) if week[d] else None for d in range(7)]

        holidays = holidays or []
        if any(not isinstance(h, datetime.date) for h in holidays):
            raise ValueError(error_messages.INVALID_HOLIDAYS)
        self.holidays = holidays

        self.max_holiday_time_up_to = 0

        self.__precompute_week_time()
        self.__precompute_holidays()

    def __generate_weekday_matrix(self):
        """Generates a matrix with the total working seconds between any combination of two weekdays.

        Args:
            days (list): A list of the total working seconds for each day of the week.
        """
        self.weekday_matrix = [
            [
                sum(
                    self.seconds_per_day[i : j + 1]
                    if j >= i
                    else self.seconds_per_day[i:] + self.seconds_per_day[: j + 1]
                )
                for j in range(7)
            ]
            for i in range(7)
        ]

    def __precompute_week_time(self):
        """Calculate and stores data related to the working hours of the week."""

        today = datetime.date.today()
        self.seconds_per_day = [
            (
                datetime.datetime.combine(today, day[1])
                - datetime.datetime.combine(today, day[0])
            ).total_seconds()
            if day is not None
            else 0
            for day in self.detail
        ]
        self.seconds_per_week = sum(self.seconds_per_day)
        self.__generate_weekday_matrix()

    def __precompute_holidays(self):
        """Calculates and stores data related to holidays.

        It stores a dictionary with the total seconds from holidays that are also working days,
        up to a given date. Also stores the maximum number of seconds from holidays.."""

        self.holiday_time_up_to = {}
        self.is_holiday = {}
        if len(self.holidays) > 0:
            day = self.holidays[0]
            while day <= self.holidays[-1]:
                holidays_up_to_now = [h for h in self.holidays if h < day]
                self.holiday_time_up_to[day.isoformat()] = sum(
                    [self.seconds_per_day[h.weekday()] for h in holidays_up_to_now]
                )
                self.is_holiday[day.isoformat()] = day in self.holidays
                day += datetime.timedelta(days=1)
            # TODO: shorten and reuse this piece of code/get the sum instead
            self.max_holiday_time_up_to = (
                self.holiday_time_up_to[self.holidays[-1].isoformat()]
                + self.seconds_per_day[self.holidays[-1].weekday()]
            )

    def __get_holiday_seconds_up_to(self, day: datetime.date):
        """Return the number of seconds from holidays up to a given date.

        It retrieves the data from the precomputed dictionary if the date is in the range of
        the holidays. Otherwise it returns 0 or the maximum number accordingly.
        """

        holiday_time = self.holiday_time_up_to.get(day.isoformat(), None)
        # print('day', day)
        # print(holiday_time)
        if holiday_time is not None:
            # print('not none?')
            # print('holiday_time', holiday_time)
            return holiday_time
        if len(self.holidays) == 0:
            return 0
        if day < self.holidays[0]:
            return 0
        if day > self.holidays[-1]:
            return self.max_holiday_time_up_to

    def __get_holiday_time_between(
        self,
        datetime1: datetime.datetime,
        datetime2: datetime.datetime,
    ):
        """Returns the number of seconds from holidays between two datetimes."""

        date1 = datetime1.date()
        date2 = datetime2.date()
        seconds1 = self.__get_holiday_seconds_up_to(date1)
        seconds2 = self.__get_holiday_seconds_up_to(date2 + datetime.timedelta(days=1))
        return seconds2 - seconds1

    def __get_time_until_next_day(self, datetime1: datetime.datetime):
        """Returns the number of working seconds until the next day."""

        time = datetime1.time()
        weekday = datetime1.weekday()
        full_day = self.seconds_per_day[weekday]

        if self.detail[weekday] is None:
            return 0
        isodate = datetime1.date().isoformat()
        if self.is_holiday.get(isodate, False):
            return 0
        if time < self.detail[weekday][0]:
            return full_day
        if time > self.detail[weekday][1]:
            return 0
        delta = (
            datetime.datetime.combine(datetime1.date(), self.detail[weekday][1])
            - datetime1
        )
        return delta.total_seconds()

    def __get_time_since_previous_day(self, datetime1: datetime.datetime):
        """Returns the number of working seconds since the previous day."""

        # TODO: dry with previouos method

        time = datetime1.time()
        weekday = datetime1.weekday()
        full_day = self.seconds_per_day[weekday]

        if self.detail[weekday] is None:
            return 0
        isodate = datetime1.date().isoformat()
        if self.is_holiday.get(isodate, False):
            return 0
        if time < self.detail[weekday][0]:
            return 0
        if time > self.detail[weekday][1]:
            return full_day
        delta = datetime1 - datetime.datetime.combine(
            datetime1.date(), self.detail[weekday][0]
        )
        return delta.total_seconds()

    def __call__(
        self,
        datetime1: datetime.datetime,
        datetime2: datetime.datetime,
    ):
        if isinstance(datetime1, str):
            datetime1 = datetime.datetime.fromisoformat(datetime1)
        if isinstance(datetime2, str):
            datetime2 = datetime.datetime.fromisoformat(datetime2)

        if datetime1 > datetime2:
            datetime1, datetime2 = datetime2, datetime1

        if datetime1.date() == datetime2.date():
            # TODO: clean and move to a method
            weekday = datetime1.weekday()
            if self.detail[weekday] is None:
                return WorkTimeDelta(0)
            isodate = datetime1.date().isoformat()
            if self.is_holiday.get(isodate, False):
                return WorkTimeDelta(0)
            day_start = datetime.datetime.combine(
                datetime1.date(), self.detail[weekday][0]
            )
            day_end = datetime.datetime.combine(
                datetime1.date(), self.detail[weekday][1]
            )
            start = max(day_start, datetime1)
            end = min(day_end, datetime2)
            delta = end - start
            if delta.total_seconds() < 0:
                return WorkTimeDelta(0)
            return WorkTimeDelta(seconds=delta.total_seconds())

        if datetime1.date() + datetime.timedelta(days=1) == datetime2.date():
            seconds1 = self.__get_time_until_next_day(datetime1)
            seconds2 = self.__get_time_since_previous_day(datetime2)
            return WorkTimeDelta(seconds=seconds1 + seconds2)

        start = datetime1.replace(hour=0, minute=0, second=0) + datetime.timedelta(
            days=1
        )
        end = datetime2.replace(hour=23, minute=59, second=59) - datetime.timedelta(
            days=1
        )
        delta = end - start

        weeks = (delta.days + 1) // 7
        seconds_from_full_weeks = weeks * self.seconds_per_week

        remaining = (delta.days + 1) % 7
        seconds_from_partial_week = (
            self.weekday_matrix[start.weekday()][end.weekday()] if remaining > 0 else 0
        )

        seconds_from_holidays = self.__get_holiday_time_between(start, end)
        seconds_from_start = self.__get_time_until_next_day(datetime1)
        seconds_from_end = self.__get_time_since_previous_day(datetime2)

        # print('seconds_from_full_weeks', seconds_from_full_weeks)
        # print('seconds_from_partial_week', seconds_from_partial_week)
        # print('seconds_from_holidays', seconds_from_holidays)
        # print('seconds_from_start', seconds_from_start)
        # print('seconds_from_end', seconds_from_end)

        total = (
            seconds_from_full_weeks
            + seconds_from_partial_week
            - seconds_from_holidays
            + seconds_from_start
            + seconds_from_end
        )
        return WorkTimeDelta(seconds=total)
