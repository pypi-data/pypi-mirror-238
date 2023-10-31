import pytest
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.observation import observable, Observation
from typing import List


def test_observable(observation: "Observation", lst_calendar: "LSTCalendar"):
    for dt in lst_calendar.dates:
        can_run = observable(observation, dt.to_yyyymmdd())
        # TODO - what to assert?
