from typing import List
from lstpressure.observation import Observation
from lstpressure.lstcalendar import LSTCalendar
from ..conftest import OBSERVATIONS


def test_self_observable(observations: List["Observation"], lst_calendar: "LSTCalendar"):
    for i, obs in enumerate(observations):
        _expected = OBSERVATIONS[i].get("_expected", {})
        _expected_count = _expected.get("result_count", None)
        observationWindows = obs.observable_dates(lst_calendar)
        if _expected and _expected_count:
            assert eval(f"len(observationWindows) {_expected_count}")
