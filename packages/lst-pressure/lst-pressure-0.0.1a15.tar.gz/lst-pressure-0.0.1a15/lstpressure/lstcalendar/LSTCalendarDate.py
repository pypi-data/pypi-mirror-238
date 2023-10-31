"""
lstcalendar.LSTCalendarDate
"""
from datetime import timedelta, date
from typing import List, Dict, Union
from lstpressure.lstindex import LSTInterval
from ..lstcalendar import LSTCalendar
from ..observation import Observation
from .Sun import Sun
from .helpers import calculate_intervals


class LSTCalendarDate:
    def __init__(self, dt, cal) -> None:
        self.dt: date = dt
        self.tomorrow_dt = dt + timedelta(days=1)
        self.sun = Sun(cal.latitude, cal.longitude, dt)
        self.tomorrow_sun = Sun(cal.latitude, cal.longitude, dt + timedelta(days=1))
        self.calendar: "LSTCalendar" = cal
        self.intervals: List["LSTInterval"] = calculate_intervals(
            cal.latitude, cal.longitude, dt, self
        )
        for interval in self.intervals:
            cal.interval_index.insert(interval.interval)

    def observations(self) -> List[Dict[str, Union["LSTInterval", "Observation"]]]:
        return [
            {
                "interval": date_interval.parent,
                "observations": [
                    observation_interval[2]
                    for observation_interval in self.calendar.observations_index.get_intervals_contained_by(
                        date_interval.interval
                    )
                    if not observation_interval[2].utc_constraints
                    or date_interval.type in observation_interval[2].utc_constraints
                ],
            }
            for date_interval in self.intervals
            if self.calendar.observations_index.get_intervals_contained_by(date_interval.interval)
        ]

    def to_yyyymmdd(self) -> str:
        return self.dt.strftime("%Y%m%d")
