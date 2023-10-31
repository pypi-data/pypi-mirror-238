"""
observation.Block
"""

from typing import List, Optional, Dict, Union
from intervaltree import Interval
from ..lstcalendar import LSTCalendar, LSTCalendarDate
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

    def observable(
        self, lstcalendar: "LSTCalendar" = None
    ) -> List[Dict[str, Union["LSTInterval", "LSTCalendarDate"]]]:
        lstcalendar = self._cal if not lstcalendar else lstcalendar

        if not lstcalendar:
            raise ValueError(
                "The 'lstcalendar' is not specified. To check observability, either associate this observation with an existing LSTCalendar instance or pass an LSTCalendar instance as an argument to this method."
            )

        results = []
        for i in lstcalendar.interval_index.get_intervals_containing(
            Interval(*normalize_interval(self.lst_window_start, self.lst_window_end))
        ):
            i_end = i[1]
            lstInterval = i[2]
            interval_type = lstInterval.type
            parent = lstInterval.parent

            if self.utc_constraints is None or (
                len(self.utc_constraints) > 0 and interval_type in self.utc_constraints
            ):
                if (
                    self.lst_window_start + self.duration < i_end
                    or self.lst_window_end + self.duration < i_end
                ):
                    results.append({"valid_interval": lstInterval, "dt": parent})

        return results
