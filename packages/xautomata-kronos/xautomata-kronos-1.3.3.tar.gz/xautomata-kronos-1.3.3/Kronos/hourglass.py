from datetime import datetime, date, timedelta, timezone
from math import copysign
from typing import Literal


class TimeZones:
    utc = timezone.utc
    rome = timezone(timedelta(hours=2))
    dict_zones = {'utc': utc, 'rome': rome}


class Format:
    # valid iso for pandas format
    ISO = 'ISO8601'


# The month lengths in non-leap and leap years respectively.
DAYS_PER_MONTHS = (
    (-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
    (-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
)


class Core:

    def __init__(self, dt=None, tz=TimeZones.rome, td=None):

        if not isinstance(dt, datetime) and not isinstance(dt, date) and dt is not None:
            raise ValueError('dt inserted is not a datetime or date')

        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]

        if type(dt) == date and dt is not None:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)

        if isinstance(dt, datetime):
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=tz)

        self.dt = dt
        self.td = td

    def __sub__(self, other):
        if self.td is None:
            td = self.dt - other.dt
            return self.__class__(td=td)
        else:
            td = self.td - other.td
            return self.__class__(td=td)

    def __add__(self, other):
        if self.td is None:
            td = self.dt + other.dt
            return self.__class__(td=td)
        else:
            td = self.td + other.td
            return self.__class__(td=td)

    def __eq__(self, other):
        if self.td is None:
            return self.dt == other.dt
        else:
            return self.td == other.td

    def __le__(self, other):
        if self.td is None:
            return self.dt <= other.dt
        else:
            return self.td <= other.td

    def __lt__(self, other):
        if self.td is None:
            return self.dt < other.dt
        else:
            return self.td < other.td

    def __ge__(self, other):
        if self.td is None:
            return self.dt >= other.dt
        else:
            return self.td > other.td

    def __gt__(self, other):
        if self.td is None:
            return self.dt > other.dt
        else:
            return self.td > other.td

    def __repr__(self):
        if self.td is None:
            return self.dt.__repr__()
        else:
            return self.td.__repr__()

    def __str__(self):
        if self.td is None:
            return self.dt.__str__()
        else:
            return self.td.__str__()

    def __hash__(self):
        if self.td is None:
            return self.dt.__hash__()
        else:
            return self.td.__hash__()

    #############################################################################
    #############################################################################
    #############################################################################

    @classmethod
    def now(cls, tz=TimeZones.rome):
        """
        Produce the current datetime

        Args:
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        return cls(datetime.now(tz=tz))

    @classmethod
    def today(cls, tz=TimeZones.rome):
        """
        Produce the current day
        Args:
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        return cls.now(tz).start_of_day()

    @classmethod
    def primetime(cls, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tz=TimeZones.rome):
        """
        Procude the Kronos element of the specified date

        Args:
            year (int): year
            month (int): month
            day (int): day
            hour (int): hour
            minute (int): minute
            second (int): second
            microsecond (int): microsecond
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        return cls(datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                            microsecond=microsecond, tzinfo=tz))

    @classmethod
    def from_isoformat(cls, iso: str, tz=TimeZones.rome):
        """
        Convert isoformat string to Kronos
        Args:
            iso (str): isoformat string
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        dt = datetime.fromisoformat(iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        return cls(dt)

    @classmethod
    def from_iso(cls, iso, tz=TimeZones.rome):
        """
        Convert isoformat string to Kronos
        Args:
            iso (str): isoformat string
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        return cls.from_isoformat(iso, tz)

    @classmethod
    def from_timestamp(cls, timestamp, tz=TimeZones.rome):
        """
        convert a timestamp to Kronos
        Args:
            timestamp (int): timestamp
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        if tz is None: tz = TimeZones.rome
        dt = datetime.fromtimestamp(timestamp, tz=tz)
        return cls(dt)

    @classmethod
    def from_ts(cls, timestamp, tz=TimeZones.rome):
        """
        convert a timestamp to Kronos
        Args:
            timestamp (int): timestamp
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        return cls.from_timestamp(timestamp, tz)

    @classmethod
    def from_datetime(cls, dt: [datetime, date], tz=TimeZones.rome):
        """
        convert a datetime or date to Kronos

        Args:
            dt (datetime, date):
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]
        if tz is None: tz = TimeZones.rome
        return cls(dt, tz=tz)

    @classmethod
    def from_dt(cls, dt: [datetime, date], tz=TimeZones.rome):
        """
        convert a datetime or date to Kronos

        Args:
            dt (datetime, date):
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        cls.from_datetime(dt, tz=tz)

    @classmethod
    def from_timedelta(cls, td: [timedelta]):
        """
        convert a timedelta to Kronos

        Args:
            td (timedelta):

        Returns: Kronos
        """
        return cls(td=td)

    @classmethod
    def from_td(cls, td: [timedelta]):
        """
        convert a timedelta to Kronos

        Args:
            td (timedelta):

        Returns: Kronos
        """
        return cls(td=td)

    @classmethod
    def from_format(cls, string: str, format: str, tz=TimeZones.rome):
        """
        convert a string with a given format to Kronos

        Args:
            string (str): string with a date
            format (str): format of the string
            tz: Timezone. Default to Rome

        Returns: Kronos
        """
        return cls(datetime.strptime(string, format), tz=tz)

    @classmethod
    def from_list_iso_to_datetime(cls, list_iso: list[str], tz=TimeZones.rome):
        """
        convert a list of string with isoformat into a list of datetime
        Args:
            list_iso (list[str]): list of isoformat string
            tz: Timezone. Default to Rome

        Returns: list[datetime]
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]

        def iso_datetime(iso):
            return cls.from_iso(iso, tz).dt

        return list(map(iso_datetime, list_iso))

    @classmethod
    def from_list_iso(cls, list_iso, tz=TimeZones.rome):
        """
        convert a list of string with isoformat into a list of Kronos
        Args:
            list_iso (list[str]): list of isoformat string
            tz: Timezone. Default to Rome

        Returns: list[Kronos]
        """
        if isinstance(tz, str): tz = TimeZones.dict_zones[tz]

        def iso_kronos(iso):
            return cls.from_iso(iso, tz)

        return list(map(iso_kronos, list_iso))

    #############################################################################
    #############################################################################
    #############################################################################

    def date(self) -> date:
        """
        return the datetime.date version of the kronos
        Returns: datetime.date
        """
        return self.dt.date()

    def datetime(self) -> datetime:
        """
        return the datetime.datetime version of the kronos
        Returns: datetime
        """
        return self.dt

    def isoformat(self) -> str:
        """
        return the isoformat version of the kronos
        Returns: str
        """
        return self.dt.isoformat()

    def iso(self) -> str:
        """
        return the isoformat version of the kronos
        Returns: str
        """
        return self.isoformat()

    def timestamp(self) -> float:
        """
        return the timestamp version of the kronos
        Returns: float
        """
        return self.dt.timestamp()

    def ts(self) -> float:
        """
        return the timestamp version of the kronos
        Returns: float
        """
        return self.timestamp()

    def timedelta(self) -> timedelta:
        """
        return the timedelta version of kronos
        Returns: timedelta
        """
        return self.td

    def td(self) -> timedelta:
        """
        return the timedelta version of the kronos
        Returns: timedelta
        """
        return self.td

    def start_of(self, period: Literal['minute', 'hour', 'day', 'week', 'month', 'year'] = 'day'):
        """
        function that set to the start of the selected period
        """
        if period == 'minute':
            dt = self.dt.replace(second=0, microsecond=0)
        elif period == 'hour':
            dt = self.dt.replace(minute=0, second=0, microsecond=0)
        elif period == 'day':
            dt = self.dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            if (self.dt.day - self.dt.weekday()) < 1:
                month = self.dt.month - 1
                year = self.dt.year
                if month < 1:
                    month = 12
                    year = self.dt.year - 1
                day = DAYS_PER_MONTHS[int(_is_leap(year))][month] - (self.dt.weekday() - self.dt.day)
            else:
                day = self.dt.day - self.dt.weekday()
                month = self.dt.month
                year = self.dt.year
            dt = self.dt.replace(year=year, month=month, day=day, hour=0, minute=0, second=0, microsecond=0)
        elif period == 'month':
            dt = self.dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == 'year':
            dt = self.dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise NotImplementedError
        return self.__class__(dt)

    def start_of_minute(self):
        """
        set to the start of the selected minut
        """
        return self.start_of('minute')

    def start_of_hour(self):
        """
        set to the start of the selected hour
        """
        return self.start_of('hour')

    def start_of_day(self):
        """
        set to the start of the selected day
        """
        return self.start_of('day')

    def start_of_week(self):
        """
        set to the start of the selected week
        """
        return self.start_of('week')

    def start_of_month(self):
        """
        set to the start of the selected month
        """
        return self.start_of('month')

    def start_of_year(self):
        """
        set to the start of the selected year
        """
        return self.start_of('year')

    def end_of(self, period: Literal['minute', 'hour', 'day', 'week', 'month', 'year'] = 'day'):
        """
        function that set to the end of the selected period
        """
        if period == 'minute':
            dt = self.dt.replace(second=59, microsecond=0)
        elif period == 'hour':
            dt = self.dt.replace(minute=59, second=59, microsecond=0)
        elif period == 'day':
            dt = self.dt.replace(hour=23, minute=59, second=59, microsecond=0)
        elif period == 'week':
            delta = 6 - self.dt.weekday()  # trasformo lunedi in 6 e domenica in 0 e poi calcolo qual'è il giorno di arrivo con day + delta
            if (self.dt.day + delta) > DAYS_PER_MONTHS[int(_is_leap(self.dt.year))][self.dt.month]:
                to_end_month = DAYS_PER_MONTHS[int(_is_leap(self.dt.year))][self.dt.month] - self.dt.day
                day = delta - to_end_month
                month = self.dt.month + 1
                year = self.dt.year
                if month > 12:
                    month = 1
                    year = self.dt.year + 1
            else:
                day = self.dt.day + delta
                month = self.dt.month
                year = self.dt.year
            dt = self.dt.replace(year=year, month=month, day=day, hour=23, minute=59, second=59, microsecond=0)
        elif period == 'month':
            dt = self.dt.replace(day=DAYS_PER_MONTHS[int(_is_leap(self.dt.year))][self.dt.month], hour=23, minute=59, second=59,
                                 microsecond=0)
        elif period == 'year':
            dt = self.dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
        else:
            raise NotImplementedError
        return self.__class__(dt)

    def end_of_minute(self):
        """
        set to the end of the selected minute
        """
        return self.end_of('minute')

    def end_of_hour(self):
        """
        set to the end of the selected hour
        """
        return self.end_of('hour')

    def end_of_day(self):
        """
        set to the end of the selected day
        """
        return self.end_of('day')

    def end_of_week(self):
        """
        set to the end of the selected week
        """
        return self.end_of('week')

    def end_of_month(self):
        """
        set to the end of the selected month
        """
        return self.end_of('month')

    def end_of_year(self):
        """
        set to the end of the selected year
        """
        return self.end_of('year')

    def add_duration(self,
                     years=0,
                     months=0,
                     weeks=0,
                     days=0,
                     hours=0,
                     minutes=0,
                     seconds=0,
                     microseconds=0):

        """
        Adds a duration to a kronos instance.
        """
        days += weeks * 7

        if (
                isinstance(self.dt, date)
                and not isinstance(self.dt, datetime)
                and any([hours, minutes, seconds, microseconds])
        ):
            raise RuntimeError("Time elements cannot be added to a date instance.")

        # Normalizing
        if abs(microseconds) > 999999:
            s = _sign(microseconds)
            div, mod = divmod(microseconds * s, 1000000)
            microseconds = mod * s
            seconds += div * s

        if abs(seconds) > 59:
            s = _sign(seconds)
            div, mod = divmod(seconds * s, 60)
            seconds = mod * s
            minutes += div * s

        if abs(minutes) > 59:
            s = _sign(minutes)
            div, mod = divmod(minutes * s, 60)
            minutes = mod * s
            hours += div * s

        if abs(hours) > 23:
            s = _sign(hours)
            div, mod = divmod(hours * s, 24)
            hours = mod * s
            days += div * s

        if abs(months) > 11:
            s = _sign(months)
            div, mod = divmod(months * s, 12)
            months = mod * s
            years += div * s

        year = self.dt.year + years
        month = self.dt.month

        if months:
            month += months
            if month > 12:
                year += 1
                month -= 12
            elif month < 1:
                year -= 1
                month += 12

        day = min(DAYS_PER_MONTHS[int(_is_leap(year))][month], self.dt.day)

        dt = self.dt.replace(year=year, month=month, day=day)

        return self.__class__(dt + timedelta(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds,
        ))

    def subtract_duration(self,
                          years=0,
                          months=0,
                          weeks=0,
                          days=0,
                          hours=0,
                          minutes=0,
                          seconds=0,
                          microseconds=0):
        """
        Subtract a duration to a kronos instance.
        """
        return self.add_duration(years=-years,
                                 months=-months,
                                 weeks=-weeks,
                                 days=-days,
                                 hours=-hours,
                                 minutes=-minutes,
                                 seconds=-seconds,
                                 microseconds=-microseconds
                                 )

    #############################################################################
    #############################################################################
    #############################################################################

    def in_periods(self, period='seconds'):
        """
        convert a time difference into the chosen time period
        """
        if period == 'seconds':
            td = int(self.td.total_seconds())
        elif period == 'minutes':
            td = int(self.td.total_seconds()/60)
        elif period == 'hours':
            td = int(self.td.total_seconds()/(60*60))
        elif period == 'days':
            td = int(self.td.total_seconds()/(60*60*24))
        elif period == 'weeks':
            td = int(self.td.total_seconds()/(60*60*24*7))
        elif period == 'months':
            td = int((self.td.total_seconds()/(60*60*24*7*(52/12))))
        elif period == 'years':
            td = int(self.td.total_seconds()/(60*60*24*7*52))
        else:
            raise NotImplementedError

        return td

    def in_seconds(self):
        """
        convert a time difference into seconds
        """
        return self.in_periods('seconds')

    def in_minutes(self):
        """
        convert a time difference into minutes
        """
        return self.in_periods('minutes')

    def in_hours(self):
        """
        convert a time difference into hours
        """
        return self.in_periods('hours')

    def in_days(self):
        """
        convert a time difference into days
        """
        return self.in_periods('days')

    def in_weeks(self):
        """
        convert a time difference into weeks
        """
        return self.in_periods('weeks')

    def in_months(self):
        """
        convert a time difference into months
        """
        return self.in_periods('months')

    def in_years(self):
        """
        convert a time difference into years
        """
        return self.in_periods('years')

    def from_interval(self, interval: int, offset: int, scale: Literal['seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'] = 'days'):
        """
        produce the start and end of a period based on the interval and offset
        """
        start = self.add_duration(**{scale: -(interval+offset)})
        stop = self.add_duration(**{scale: -offset})
        return start, stop

    #############################################################################
    #############################################################################
    #############################################################################


def _sign(x):
    return int(copysign(1, x))


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
