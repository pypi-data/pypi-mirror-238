"""
lstpressure.lstcalendar
"""
from datetime import datetime
from intervaltree import Interval
from .LSTIntervalType import LSTIntervalType
from ..lstcalendar import Sun, LSTCalendarDate
from ..observation import Observation
from typing import Union
from ..utils import normalize_yyyymmdd_to_datetime


def normalize_interval(start, end, days=1):
    if end < start:
        end += 24
    end += 24 * (days - 1)
    return (start, end)


class LSTInterval:
    """
    A wrapper around the intervaltree Interval class
    for easer access in the context of lst-pressure
    """

    def __init__(
        self,
        start: float,
        end: float,
        parent: Union["LSTCalendarDate", "Observation"] = None,
        dt: datetime = None,
        type: "LSTIntervalType" = None,
        sun: "Sun" = None,
        tomorrow_sun: "Sun" = None,
    ) -> None:
        self._type = type if type else None
        self._dt = normalize_yyyymmdd_to_datetime(dt) if dt else None
        self._sun = sun if sun else None
        self._tomorrow_sun = tomorrow_sun if tomorrow_sun else None
        self._parent = parent if parent else None
        self._interval = Interval(start, end, self)

    @property
    def parent(self):
        return self._parent

    @property
    def interval(self):
        return self._interval

    @property
    def start(self):
        return self._interval[0]

    @property
    def end(self):
        return self._interval[1]

    @property
    def type(self):
        return self._type

    @property
    def dt(self):
        return self._dt

    @property
    def sun(self):
        return self._sun

    @property
    def tomorrow_sun(self):
        return self._tomorrow_sun
