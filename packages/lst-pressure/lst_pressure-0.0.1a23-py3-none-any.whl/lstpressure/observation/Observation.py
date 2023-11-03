"""
observation.Block
"""

from typing import List, Optional
from intervaltree import Interval

# TODO
from ..lstcalendar import LSTCalendar, LSTCalendarDate
from ..lstcalendar.ObservationWindow import ObservationWindow
from ..lstindex import LSTIntervalType, normalize_interval


class Observation:
    """
    Represents an observation block with given Local Sidereal Time (LST) window and UTC constraints.

    Attributes
    ----------
    id: any
        The ID of the observation block
    lst_window_start : float
        The starting value of the LST window.
    lst_window_end : float
        The ending value of the LST window.
    utc_constraints : List[LSTInterval]
        The UTC constraints for the observation block represented as a list of LSTInterval values. Defaults to 0.
    """

    def __init__(
        self,
        id: any,
        lst_window_start: float,
        lst_window_end: float,
        utc_constraints: List["LSTIntervalType"] = None,
        duration: float = None,
    ) -> None:
        """
        Initializes an instance of Block.

        Parameters
        ----------
        id: any
            The ID of the observation block
        lst_window_start : float
            The starting value of the LST window.
        lst_window_end : float
            The ending value of the LST window.
        utc_constraints : List[LSTInterval]
            The UTC constraints for the observation block represented as a list of LSTInterval values. Defaults to 0.
        """
        self.id = id
        self.lst_window_start = lst_window_start
        self.lst_window_end = lst_window_end
        self.utc_constraints = utc_constraints
        self._duration = duration if duration else lst_window_end - lst_window_start
        self._cal: Optional["LSTCalendar"] = None  # Reference to the calendar
        self._interval = Interval(
            *normalize_interval(self.lst_window_start, self.lst_window_end), self
        )

    @property
    def duration(self) -> float:
        """
        Required observation duration in hours (decimal)
        """
        return self._duration

    @property
    def interval(self) -> "Interval":
        return self._interval

    @property
    def calendar(self) -> "LSTCalendar":
        if not self._cal:
            raise ValueError("Block has not been added to any LSTCalendar.")
        return self._cal

    @calendar.setter
    def calendar(self, cal: "LSTCalendar"):
        self._cal = cal

    def observable_dates(self, lstcalendar: "LSTCalendar" = None) -> List["ObservationWindow"]:
        lstcalendar = self._cal if not lstcalendar else lstcalendar

        if not lstcalendar:
            raise ValueError(
                "'lstcalendar' is not specified. To check observability, either associate this observation with an existing LSTCalendar instance or pass an LSTCalendar instance as an argument to this method."
            )

        results = []
        query = Interval(*normalize_interval(self.lst_window_start, self.lst_window_end))

        # If the observation interval ends after 24, then an additional interval is required
        query2 = Interval(0, self.lst_window_end - 24) if (self.lst_window_end > 24) else None

        # Note that overlap() returns a set
        calendar_intervals = (
            lstcalendar.interval_index.overlap(query) | lstcalendar.interval_index.overlap(query2)
            if query2
            else lstcalendar.interval_index.overlap(query)
        )

        for i in calendar_intervals:
            i_end = i[1]
            lstInterval = i[2]
            interval_type = lstInterval.type

            if (self.utc_constraints is None or len(self.utc_constraints) == 0) or (
                len(self.utc_constraints) > 0 and interval_type in self.utc_constraints
            ):
                if (
                    self.lst_window_start + self.duration < i_end
                    or self.lst_window_end + self.duration < i_end
                ):
                    results.append(ObservationWindow(lstInterval, self))

        return results
