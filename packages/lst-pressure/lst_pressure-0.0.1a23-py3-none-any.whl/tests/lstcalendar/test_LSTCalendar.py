import pytest
from typing import List
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.observation import Observation
from ..conftest import OBSERVATIONS


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("20230404", "20230404", ["20230404"]),
        ("20230404", "20230405", ["20230404", "20230405"]),
        ("20220101", "20220105", ["20220101", "20220102", "20220103", "20220104", "20220105"]),
        (
            "20231025",
            "20231031",
            ["20231025", "20231026", "20231027", "20231028", "20231029", "20231030", "20231031"],
        ),
    ],
)
def test_Calendar(start, end, expected):
    """
    The calendar should convert start/end params into the correct range
    """
    assert expected == [d.dt.strftime("%Y%m%d") for d in LSTCalendar(start, end)._dates]


# Invalid start/end should NOT work
@pytest.mark.parametrize(
    "start, end",
    [("invalidStart", "20220105"), ("20220101", "invalidEnd"), ("20220105", "20220101")],
)
def test_calendar_raises_exception_for_invalid_dates(start, end):
    with pytest.raises(ValueError):
        LSTCalendar(start, end)


# The observations property should return all the observations
def test_self_observations(observations: List["Observation"], lst_calendar: "LSTCalendar"):
    lst_calendar.load_observations(observations)
    observations = lst_calendar.observations
    assert len(observations) == len(OBSERVATIONS)


# The observations property should return all the observations
def test_self_observable_observations(
    observations: List["Observation"], lst_calendar: "LSTCalendar"
):
    observable_observations = lst_calendar.observable_observations(observations)
    # TODO
