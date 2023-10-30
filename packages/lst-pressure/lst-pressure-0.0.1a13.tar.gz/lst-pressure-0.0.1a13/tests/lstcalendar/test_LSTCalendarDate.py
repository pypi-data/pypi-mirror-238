from lstpressure.lstcalendar import LSTCalendar
from typing import List
from lstpressure.Observation import Observation


def test_self_eligible_observations(observations: List["Observation"], lst_calendar: "LSTCalendar"):
    lst_calendar.load_observations(observations)
    for i, date in enumerate(lst_calendar.dates):
        eligible_observations = date.eligible_observations()
