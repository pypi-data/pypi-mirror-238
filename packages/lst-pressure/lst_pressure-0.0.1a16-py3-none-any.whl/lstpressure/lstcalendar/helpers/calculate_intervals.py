from datetime import datetime, timedelta
from typing import List, Union
from ..Sun import Sun
from ...lstindex import LSTInterval, LSTIntervalType, normalize_interval
from ...utils import utc_to_lst, normalize_coordinates


def calculate_intervals(
    latitude: Union[str, float], longitude: Union[str, float], today_dt: "datetime", self
) -> List["LSTInterval"]:
    """
    Calculate intervals for a given date based on sun statistics.

    Parameters
    ----------
    today_dt : datetime
        The specific day for which intervals are being calculated.
    today_sun : Dict
        The sun statistics for the specific day.

    Returns
    -------
    List[Interval]
        A list of calculated intervals.
    """
    latitude, longitude = normalize_coordinates(latitude, longitude)
    today = today_dt  # TODO normalize dates
    today_sun = Sun(latitude, longitude, today)
    tomorrow = today + timedelta(days=1)
    tomorrow_sun = Sun(latitude, longitude, tomorrow)
    today_sunrise = today_sun.sunrise
    today_sunrise_lst = utc_to_lst(today_sunrise, latitude, longitude)
    today_sunset = today_sun.sunset
    today_sunset_lst = utc_to_lst(today_sunset, latitude, longitude)
    today_dusk = today_sun.dusk
    today_dusk_lst = utc_to_lst(today_dusk, latitude, longitude)
    tomorrow_dawn = tomorrow_sun.dawn
    tomorrow_dawn_lst = utc_to_lst(tomorrow_dawn, latitude, longitude)
    tomorrow_sunrise = tomorrow_sun.sunrise
    tomorrow_sunrise_lst = utc_to_lst(tomorrow_sunrise, latitude, longitude)

    return (
        # AVOID_SUNRISE_SUNSET
        LSTInterval(
            *normalize_interval(today_sunrise_lst, today_sunset_lst),
            self,
            today,
            LSTIntervalType.AVOID_SUNRISE_SUNSET,
            today_sun,
            tomorrow_sun,
        ),
        # AVOID_SUNSET_SUNRISE
        LSTInterval(
            *normalize_interval(today_sunset_lst, tomorrow_sunrise_lst),
            self,
            today,
            LSTIntervalType.AVOID_SUNSET_SUNRISE,
            today_sun,
            tomorrow_sun,
        ),
        # NIGHT_ONLY
        LSTInterval(
            *normalize_interval(today_dusk_lst, tomorrow_dawn_lst),
            self,
            today,
            LSTIntervalType.NIGHT_ONLY,
            today_sun,
            tomorrow_sun,
        ),
        # ALL_DAY
        LSTInterval(0, 24, self, today, LSTIntervalType.ALL_DAY, today_sun, tomorrow_sun),
    )
