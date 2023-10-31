from Kronos.hourglass import Core, TimeZones, Format


def now(tz=TimeZones.rome):
    """
    Produce the current datetime

    Args:
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.now(tz=tz)


def today(tz=TimeZones.rome):
    """
    Produce the current day
    Args:
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.today(tz=tz)


def primetime(year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tz=TimeZones.rome):
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
    return Core.primetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond, tz=tz)


def from_isoformat(iso, tz=TimeZones.rome):
    """
    Convert isoformat string to Kronos
    Args:
        iso (str): isoformat string
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_isoformat(iso=iso, tz=tz)


def from_iso(iso, tz=TimeZones.rome):
    """
    Convert isoformat string to Kronos
    Args:
        iso (str): isoformat string
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_iso(iso=iso, tz=tz)


def from_timestamp(timestamp, tz=TimeZones.rome):
    """
    convert a timestamp to Kronos
    Args:
        timestamp (int): timestamp
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_timestamp(timestamp=timestamp, tz=tz)


def from_ts(timestamp, tz=TimeZones.rome):
    """
    convert a timestamp to Kronos
    Args:
        timestamp (int): timestamp
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_ts(timestamp=timestamp, tz=tz)


def from_datetime(dt, tz=TimeZones.rome):
    """
    convert a datetime or date to Kronos

    Args:
        dt (datetime, date):
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_datetime(dt=dt, tz=tz)


def from_dt(dt, tz=TimeZones.rome):
    """
    convert a datetime or date to Kronos

    Args:
        dt (datetime, date):
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_dt(dt=dt, tz=tz)


def from_timedelta(td):
    """
    convert a timedelta to Kronos

    Args:
        td (timedelta):

    Returns: Kronos
    """
    return Core.from_timedelta(td)


def from_td(td):
    """
    convert a timedelta to Kronos

    Args:
        td (timedelta):

    Returns: Kronos
    """
    return Core.from_td(td)


def from_format(string: str, format: str, tz=TimeZones.rome):
    """
    convert a string with a given format to Kronos

    Args:
        string (str): string with a date
        format (str): format of the string
        tz: Timezone. Default to Rome

    Returns: Kronos
    """
    return Core.from_format(string=string, format=format, tz=tz)


def from_list_iso_to_datetime(list_iso, tz=TimeZones.rome):
    """
    convert a list of string with isoformat into a list of datetime
    Args:
        list_iso (list[str]): list of isoformat string
        tz: Timezone. Default to Rome

    Returns: list[datetime]
    """
    return Core.from_list_iso_to_datetime(list_iso=list_iso, tz=tz)


def from_list_iso(list_iso, tz=TimeZones.rome):
    """
    convert a list of string with isoformat into a list of Kronos
    Args:
        list_iso (list[str]): list of isoformat string
        tz: Timezone. Default to Rome

    Returns: list[Kronos]
    """
    return Core.from_list_iso(list_iso=list_iso, tz=tz)
