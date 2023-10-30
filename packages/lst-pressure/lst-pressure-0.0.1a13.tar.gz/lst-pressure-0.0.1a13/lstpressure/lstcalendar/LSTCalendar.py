"""
lstcalendar.LSTCalendar
"""
from datetime import timedelta, datetime
from typing import Union, List
from ..Observation import Observation
from .LSTCalendarDate import LSTCalendarDate
from ..lstindex.LSTIndex import LSTIndex
from ..utils import (
    normalize_yyyymmdd_to_datetime,
    normalize_coordinates,
)


class LSTCalendar:
    """
    Calendar tailored for LST (Local Sidereal Time) related interval lookups.

    Attributes
    ----------
    start : datetime
        The beginning of the date range for the calendar.
    end : datetime
        The conclusion of the date range for the calendar.
    latitude : float
        The geographic latitude in decimal degrees. Defaults to 0.
    longitude : float
        The geographic longitude in decimal degrees. Defaults to 0.
    interval_index : Idx
        An index to manage intervals efficiently.
    dates : List[LSTCalendarDate]
        A list containing dates and corresponding sun statistics within the range.

    Methods
    -------
    __init__(start, end, latitude=0, longitude=0)
        Initialize the LSTCalendar object.
    _calculate_intervals(today_dt, today_sun, tomorrow_sun)
        Calculate intervals for a given date based on sun statistics.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(
        self,
        start: Union[str, datetime],
        end: Union[str, datetime],
        latitude: Union[str, float] = 0,
        longitude: Union[str, float] = 0,
    ):
        """
        Initialize the LSTCalendar object.

        Parameters
        ----------
        start : Union[str, datetime]
            Start date of the calendar range.
        end : Union[str, datetime]
            End date of the calendar range.
        latitude : Union[str, float], optional
            Latitude for the location. Defaults to 0.
        longitude : Union[str, float], optional
            Longitude for the location. Defaults to 0.

        Raises
        ------
        ValueError
            If the start date is after the end date.
        """
        start = normalize_yyyymmdd_to_datetime(start)
        end = normalize_yyyymmdd_to_datetime(end)

        if start > end:
            raise ValueError("start day should be <= end day")

        latitude, longitude = normalize_coordinates(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
        self._interval_index = LSTIndex()
        self._observations_index = LSTIndex()
        self._dates = [
            LSTCalendarDate(start + timedelta(days=d), self)
            for d in range(0, (end - start).days + 1)
        ]

    @property
    def interval_index(self) -> LSTIndex:
        return self._interval_index

    @property
    def observations_index(self) -> LSTIndex:
        return self._observations_index

    @property
    def dates(self) -> List["LSTCalendarDate"]:
        return self._dates

    def load_observations(self, observations: List["Observation"]):
        for observation in observations:
            observation.calendar = self
            self.observations_index.insert(observation.interval)

    def eligible_observations(self) -> List["Observation"]:
        return [observation for date in self.dates for observation in date.eligible_observations()]
