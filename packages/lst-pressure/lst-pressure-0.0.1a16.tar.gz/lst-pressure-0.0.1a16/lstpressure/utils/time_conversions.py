"""
lstpressure.time_conversions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module containing time conversion utilities, including conversion from UTC to Local Sidereal Time (LST) 
and conversion from a time string to its decimal hour representation.
"""

from astropy.time import Time
from astropy import units as u
from astropy.utils import iers
from functools import lru_cache
from typing import Union
from datetime import datetime
from .normalize_coordinates import normalize_coordinates
from .normalize_date import normalize_datetime

# iers.conf.auto_download = False
# iers.conf.auto_max_age = None
# iers.conf.iers_degraded_accuracy = "warn"

# Constants
LST_DAY_DEC = 23.9344696
"""Length of a sidereal day in decimal hours."""


@lru_cache(maxsize=None)
def utc_to_lst(
    iso_date: Union[str, datetime], lat: Union[str, float], long: Union[str, float]
) -> float:
    """
    Convert a given UTC datetime to Local Sidereal Time (LST).

    Parameters:
    -----------
    iso_date : Union[str, datetime]
        An ISO 8601 date string or datetime object representing UTC time.
    lat : Union[str, float]
        Latitude coordinate, can be a string (e.g., "52d40m") or float.
    long : Union[str, float]
        Longitude coordinate, can be a string (e.g., "4d55m") or float.

    Returns:
    --------
    float
        The Local Sidereal Time in decimal hours.

    Example:
    --------
    >>> utc_to_lst("2023-10-26T12:00:00", "52d40m", "4d55m")
    14.5567
    """
    # Normalize coordinates
    lat, long = normalize_coordinates(lat, long)

    # Convert ISO date to astropy Time object
    t = Time(normalize_datetime(iso_date))

    # Compute sidereal time
    lst = t.sidereal_time("mean", longitude=long)

    return lst.to_value()


@lru_cache(maxsize=None)
def normalize_time_to_decimal(time: Union[str, float]) -> float:
    """
    Convert a time string of format hours:min:sec to decimal hours.

    Parameters:
    -----------
    time : str
        A time string formatted as "hours:min:sec".

    Returns:
    --------
    float
        The time represented in decimal hours.

    Raises:
    -------
    ValueError
        If the input time is not a string or if it doesn't have the expected format.

    Example:
    --------
    >>> time_to_decimal("2:30:0")
    2.5
    """
    if isinstance(time, float):
        return time

    if not isinstance(time, str):
        raise ValueError("Input should be a string in format hours:min:sec")

    # Split the time string by colon to get hours, minutes, and seconds
    components = time.split(":")

    if len(components) != 3:
        raise ValueError("Time string should have format hours:min:sec")

    hours, minutes, seconds = map(int, components)

    # Convert time components to decimal hours
    decimal_hours = hours + (minutes / 60) + (seconds / 3600)

    return decimal_hours
