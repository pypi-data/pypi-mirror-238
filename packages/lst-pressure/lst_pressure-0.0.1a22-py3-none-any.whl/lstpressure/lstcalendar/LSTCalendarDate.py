"""
lstcalendar.LSTCalendarDate
"""
from datetime import timedelta, date
from typing import List
from lstpressure.lstindex import LSTInterval
from ..lstcalendar import LSTCalendar
from .ObservationWindow import ObservationWindow
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

    # TODO - outdated logic
    def observations(self) -> List["ObservationWindow"]:
        result = []

        for date_interval in self.intervals:
            if self.calendar.observations_index.envelop(date_interval.interval):
                for observation_interval in self.calendar.observations_index.envelop(
                    date_interval.interval
                ):
                    if (
                        not observation_interval[2].utc_constraints
                        or date_interval.type in observation_interval[2].utc_constraints
                    ):
                        result.append(ObservationWindow(date_interval, observation_interval[2]))

        return result

    def to_yyyymmdd(self) -> str:
        return self.dt.strftime("%Y%m%d")
