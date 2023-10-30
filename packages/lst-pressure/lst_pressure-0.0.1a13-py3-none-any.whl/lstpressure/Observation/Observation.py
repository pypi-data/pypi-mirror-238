"""
observation.Block
"""

from typing import List, Optional
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
        self.duration = duration
        self._cal: Optional["LSTCalendar"] = None  # Reference to the calendar
        self._interval = Interval(
            *normalize_interval(self.lst_window_start, self.lst_window_end), self
        )

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

    def eligible_dates(self, lstcalendar: "LSTCalendar") -> List["LSTCalendarDate"]:
        return [
            i[2].parent
            for i in lstcalendar.interval_index.get_intervals_containing(
                Interval(*normalize_interval(self.lst_window_start, self.lst_window_end))
            )
            if self.utc_constraints is None
            or (len(self.utc_constraints) > 0 and i[2].type in self.utc_constraints)
        ]
