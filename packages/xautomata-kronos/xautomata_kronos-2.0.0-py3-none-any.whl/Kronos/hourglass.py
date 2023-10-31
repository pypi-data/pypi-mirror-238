from datetime import datetime, date
from Kronos.periods import periods
from Kronos.converters import converters
from Kronos.costructors import costructors, TimeZones


class Format:
    # valid iso for pandas format
    ISO = 'ISO8601'


class Core(periods, converters, costructors):

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
