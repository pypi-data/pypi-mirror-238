"""
lstcalendar.LSTInterval
"""

from enum import Enum, auto


class LSTIntervalType(Enum):
    """
    Different types of LST intervals to avoid specific times of the day.

    Attributes
    ----------
    AVOID_SUNRISE_SUNSET : Enum
        Represents intervals that avoid both sunrise and sunset.
    NIGHT_ONLY : Enum
        Represents intervals that only consider night time.
    """

    ALL_DAY = auto()
    AVOID_SUNRISE_SUNSET = auto()
    AVOID_SUNSET_SUNRISE = auto()
    NIGHT_ONLY = auto()
    OBSERVATION_WINDOW = auto()
