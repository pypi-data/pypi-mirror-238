"""
lstcalendar.LSTCalendarDate
"""
from datetime import timedelta, date
from typing import List
from lstpressure.lstindex import LSTInterval
from ..lstcalendar import LSTCalendar
from intervaltree import Interval
from .ObservationWindow import ObservationWindow
from .Sun import Sun
from .helpers import calculate_intervals


class LSTCalendarDate:
    def __init__(self, dt, cal) -> None:
        if not cal:
            raise TypeError(
                'Missing "cal" argument, LSTCalendarDate instances must be instantiated via instances of LSTCalendar so that the self.cal can be assigned'
            )

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

    def observable_observations(self) -> List["ObservationWindow"]:
        result = []

        # Cycle through dt intervals
        for lstInterval in self.intervals:
            i_end = lstInterval.end
            interval_type = lstInterval.type
            query = lstInterval.interval
            query2 = Interval(0, i_end - 24) if i_end > 24 else None

            # Note that overlap() returns a Set
            o_intervals = (
                self.calendar.observations_index.overlap(query)
                | self.calendar.observations_index.overlap(query2)
                if query2
                else self.calendar.observations_index.overlap(query)
            )

            for o_interval in o_intervals:
                lst_window_start, lst_window_end, o = o_interval
                utc_constraints = o.utc_constraints
                duration = o.duration

                if (utc_constraints is None or len(utc_constraints) == 0) or (
                    len(utc_constraints) > 0 and interval_type in utc_constraints
                ):
                    if lst_window_start + duration < i_end or lst_window_end + duration < i_end:
                        result.append(ObservationWindow(lstInterval, o))

        return result

    def to_yyyymmdd(self) -> str:
        return self.dt.strftime("%Y%m%d")
