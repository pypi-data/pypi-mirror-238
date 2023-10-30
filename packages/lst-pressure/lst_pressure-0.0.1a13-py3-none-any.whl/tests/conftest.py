from lstpressure.lstindex import LSTIntervalType
import pytest
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.Observation import Observation

OBSERVATIONS = [
    {
        "id": "obs-1",
        "lst_window_start": 6.5,
        "lst_window_end": 10.2,
        "utc_constraints": [LSTIntervalType.ALL_DAY],
        "_expected": {},
    },
    {
        "id": "obs-2",
        "lst_window_start": 21.5,
        "lst_window_end": 20,
        "duration": 2,
        "utc_constraints": [LSTIntervalType.NIGHT_ONLY],
        "_expected": {
            # "result_count": ">= 1"
        },
    },
    {
        "id": "obs-3",
        "lst_window_start": 22,
        "lst_window_end": 23,
        "utc_constraints": [LSTIntervalType.NIGHT_ONLY],
        "_expected": {},
    },
]


@pytest.fixture
def observations():
    return [
        Observation(
            id=obs.get("id"),
            lst_window_start=obs.get("lst_window_start"),
            lst_window_end=obs.get("lst_window_end"),
            utc_constraints=obs.get("utc_constraints"),
            duration=obs.get("duration"),
        )
        for obs in OBSERVATIONS
    ]


@pytest.fixture
def lst_calendar():
    coordinates = ["-30:42:39.8", "21:26:38.0"]
    start_end = ["20231001", "20231015"]
    return LSTCalendar(*start_end, *coordinates)
