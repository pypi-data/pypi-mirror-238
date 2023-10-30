import pytest
from typing import List
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.Observation import Observation


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


def test_self_eligible_observations(observations: List["Observation"], lst_calendar: "LSTCalendar"):
    lst_calendar.load_observations(observations)
    eligible_observations = lst_calendar.eligible_observations()
