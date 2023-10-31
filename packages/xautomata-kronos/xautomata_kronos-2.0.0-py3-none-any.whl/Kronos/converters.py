from datetime import date, datetime, timedelta

class converters:

    def __init__(self, dt=None, td=None):
        self.dt = dt
        self.td = td

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