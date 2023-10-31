from typing import List
from datetime import timezone, timedelta, datetime, date
from Kronos.sliders import sliders


class TimeZones:
    utc = timezone.utc
    rome = timezone(timedelta(hours=1))
    dict_zones = {'utc': utc, 'rome': rome}


class costructors(sliders):

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
    def from_list_iso_to_datetime(cls, list_iso: List[str], tz=TimeZones.rome):
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
