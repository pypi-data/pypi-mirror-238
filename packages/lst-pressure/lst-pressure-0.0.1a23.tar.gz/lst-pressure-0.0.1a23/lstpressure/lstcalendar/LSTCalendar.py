"""
lstcalendar.LSTCalendar
"""
from datetime import timedelta, datetime
from typing import Union, List, Dict, Optional
from ..observation import Observation
from .ObservationWindow import ObservationWindow
from .LSTCalendarDate import LSTCalendarDate
from ..lstindex import LSTIndex, LSTInterval
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
        end: Optional[Union[str, datetime]] = None,
        latitude: Union[str, float] = "-30:42:39.8",
        longitude: Union[str, float] = "21:26:38.0",
        observations: List["Observation"] = [],
    ):
        """
        Initialize the LSTCalendar object.

        Parameters
        ----------
        start : Union[str, datetime]
            Start date of the calendar range.
        end : (Optional )Union[str, datetime]
            End date of the calendar range. Defaults to start
        latitude : Union[str, float], optional
            Latitude for the location. Defaults to 0.
        longitude : Union[str, float], optional
            Longitude for the location. Defaults to 0.
        observations : List[Observation], optional
            List of observation instances. called load_observations method under the hood

        Raises
        ------
        ValueError
            If the start date is after the end date.
        """
        start = normalize_yyyymmdd_to_datetime(start)
        end = start if not end else normalize_yyyymmdd_to_datetime(end)

        if start > end:
            raise ValueError("start day should be <= end day")

        latitude, longitude = normalize_coordinates(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
        self._interval_index = LSTIndex()
        self._dates = [
            LSTCalendarDate(start + timedelta(days=d), self)
            for d in range(0, (end - start).days + 1)
        ]
        self.load_observations(observations)

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
        """
        Load a list of observations, set the calendar attribute for each observation,
        and insert their intervals into the observation index.

        Args:
            observations (List[Observation]): A list of observation instances.

        Returns:
            None
        """
        self._observations = []
        self._observations_index = LSTIndex()
        for observation in observations:
            observation.calendar = self
            self._observations.append(observation)
            self.observations_index.insert(observation.interval)

    @property
    def observations(self) -> List[Dict[str, Union["LSTInterval", "Observation"]]]:
        """
        Property to retrieve the list of observations.

        Returns:
            List[Dict[str, Union[LSTInterval, Observation]]]: A list of observations.
        """
        return self._observations

    @observations.setter
    def observations(self, observations: List["Observation"]) -> None:
        """
        Setter for the observations property. It serves as an alias for the load_observations method.

        Args:
            observations (List[Observation]): A list of observation instances.

        Returns:
            None
        """
        self.load_observations(observations)

    def observable_observations(
        self, observations: Optional[List["Observation"]] = None
    ) -> List["ObservationWindow"]:
        """
        Retrieve observable observations for the dates maintained by this calendar.

        This method processes a list of dates within the calendar and aggregates their observable observations into observation windows. If a list of observations is provided, it replaces the current observations of the calendar with the new list.

        :param observations: A list of Observation objects to process, which is optional. If provided, it overwrites any existing observations in the calendar.
        :type observations: Optional[List["Observation"]]
        :raises TypeError: If no observations have been loaded into the calendar and none are provided.
        :return: A list of aggregated observation windows, each representing observable observations for a specific date in the calendar.
        :rtype: List["ObservationWindow"]

        If no observations are passed to the method and the calendar has no loaded observations, it raises a TypeError indicating that no observations are available for processing.

        Example usage:

        .. code-block:: python

            calendar = Calendar()
            calendar.load_dates(dates)
            try:
                observation_windows = calendar.observable_observations()
            except TypeError as e:
                print(e)

        """
        # If observations provided as an argument, assume the intent is to overwrite
        if observations:
            self.load_observations(observations)

        if not self.observations:
            raise TypeError(
                "No observations have been loaded on this calendar, and no observations have been provided as an argument"
            )

        results = []
        for dt in self.dates:
            results = results + dt.observable_observations()

        return results
