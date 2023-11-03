from datetime import datetime, timedelta
from typing import List, Union
from ..Sun import Sun
from ...lstindex import LSTInterval, LSTIntervalType, normalize_interval
from ...utils import normalize_coordinates


def calculate_intervals(
    latitude: Union[str, float], longitude: Union[str, float], today_dt: "datetime", self
) -> List["LSTInterval"]:
    """
    Calculate intervals for a given date based on sun statistics.

    Parameters
    ----------

    Returns
    -------
    List[Interval]
        A list of calculated intervals.
    """
    latitude, longitude = normalize_coordinates(latitude, longitude)

    today = today_dt
    today_sun = Sun(latitude, longitude, today)
    today_dawn_lst = today_sun.dawn_lst
    today_sunrise_lst = today_sun.sunrise_lst
    today_sunset_lst = today_sun.sunset_lst
    today_dusk_lst = today_sun.dusk_lst

    tomorrow = today + timedelta(days=1)
    tomorrow_sun = Sun(latitude, longitude, tomorrow)
    tomorrow_dawn_lst = tomorrow_sun.dawn_lst
    tomorrow_sunrise_lst = tomorrow_sun.sunrise_lst

    result = []

    # ALL DAY
    result.append(LSTInterval(0, 24, self, today, LSTIntervalType.ALL_DAY, today_sun, tomorrow_sun))

    # AVOID_SUNRISE_SUNSET
    AVOID_SUNRISE_SUNSET = LSTInterval(
        *normalize_interval(today_sunrise_lst, today_sunset_lst),
        self,
        today,
        LSTIntervalType.AVOID_SUNRISE_SUNSET,
        today_sun,
        tomorrow_sun,
    )
    result.append(AVOID_SUNRISE_SUNSET)
    if AVOID_SUNRISE_SUNSET.end > 24:
        result.append(
            LSTInterval(
                0,
                today_sunset_lst,
                self,
                today,
                LSTIntervalType.AVOID_SUNRISE_SUNSET,
                today_sun,
                tomorrow_sun,
            )
        )

    # AVOID_SUNSET_SUNRISE
    AVOID_SUNSET_SUNRISE = LSTInterval(
        *normalize_interval(today_sunset_lst, tomorrow_sunrise_lst),
        self,
        today,
        LSTIntervalType.AVOID_SUNSET_SUNRISE,
        today_sun,
        tomorrow_sun,
    )
    result.append(AVOID_SUNSET_SUNRISE)

    if AVOID_SUNSET_SUNRISE.end > 24:
        result.append(
            LSTInterval(
                0,
                today_sunrise_lst,
                self,
                today,
                LSTIntervalType.AVOID_SUNSET_SUNRISE,
                today_sun,
                tomorrow_sun,
            )
        )

    # NIGHT_ONLY
    NIGHT_ONLY = LSTInterval(
        *normalize_interval(today_dusk_lst, tomorrow_dawn_lst),
        self,
        today,
        LSTIntervalType.NIGHT_ONLY,
        today_sun,
        tomorrow_sun,
    )
    result.append(NIGHT_ONLY)

    if NIGHT_ONLY.end > 24:
        result.append(
            LSTInterval(
                0,
                today_dawn_lst,
                self,
                today,
                LSTIntervalType.NIGHT_ONLY,
                today_sun,
                tomorrow_sun,
            )
        )

    return result
