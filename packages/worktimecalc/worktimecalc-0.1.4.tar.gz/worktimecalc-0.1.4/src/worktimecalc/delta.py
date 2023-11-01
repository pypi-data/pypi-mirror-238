from datetime import timedelta


class WorkTimeDelta(timedelta):
    """Subclass of datetime.timedelta with some extra properties."""

    @property
    def seconds(self):
        return self.total_seconds()

    @property
    def as_dhms(self):
        return {
            'days': self.days,
            'hours': int(self.seconds // 3600 % 24),
            'minutes': int(self.seconds // 60 % 60),
            'seconds': int(self.seconds % 60),
        }

    @property
    def as_hms(self):
        seconds = self.total_seconds()
        return {
            'hours': int(seconds // 3600),
            'minutes': int(seconds // 60 % 60),
            'seconds': int(seconds % 60),
        }