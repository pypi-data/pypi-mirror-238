from typing import List
from lstpressure.Observation import Observation
from lstpressure.lstcalendar import LSTCalendar, LSTCalendarDate
from ..conftest import OBSERVATIONS


def test_self_eligible_dates(observations: List["Observation"], lst_calendar: "LSTCalendar"):
    for i, obs in enumerate(observations):
        eligible_dates: List["LSTCalendarDate"] = obs.eligible_dates(lst_calendar)
        _expected = OBSERVATIONS[i].get("_expected")
        _expected_count = _expected.get("result_count", None)
        if _expected_count:
            assert eval(f"len(eligible_dates) {_expected_count}")
