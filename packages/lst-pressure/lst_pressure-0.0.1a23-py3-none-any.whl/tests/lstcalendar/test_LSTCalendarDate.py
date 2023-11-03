import pytest
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.lstindex import LSTIntervalType
from lstpressure.observation import Observation
from typing import List

OBSERVATIONS = [
    Observation(
        o.get("id"),
        o.get("lst_window_start"),
        o.get("lst_window_end"),
        o.get("utc_constraints"),
        o.get("duration"),
    )
    for o in [
        {
            "id": "O1",
            "lst_window_start": 6.5,
            "lst_window_end": 10.2,
            "utc_constraints": [LSTIntervalType.ALL_DAY],
            "duration": 1,
        },
        {
            "id": "O2",
            "lst_window_start": 8.5,
            "lst_window_end": 10.2,
            "utc_constraints": [LSTIntervalType.NIGHT_ONLY],
            "duration": 1,
        },
        {
            "id": "O3",
            "lst_window_start": 21.5,
            "lst_window_end": 20,
            "utc_constraints": [LSTIntervalType.NIGHT_ONLY],
            "duration": 0.5,
        },
        {
            "id": "O4",
            "lst_window_start": 12,
            "lst_window_end": 22,
            "utc_constraints": [LSTIntervalType.NIGHT_ONLY],
            "duration": 1.5,
        },
        {
            "id": "O5",
            "lst_window_start": 9,
            "lst_window_end": 10,
            "utc_constraints": [LSTIntervalType.AVOID_SUNRISE_SUNSET],
            "duration": 0.5,
        },
    ]
]


@pytest.mark.parametrize(
    "dt_range, latlng, expected",
    [
        (["20231101"], ["-30:42:39.8", "21:26:38.0"], ["O1", "O3", "O4", "O5"]),
        (["20231101", "20231101"], ["-30:42:39.8", "21:26:38.0"], ["O1", "O3", "O4", "O5"]),
    ],
)
def test_self_observations(dt_range, latlng, expected: "List"):
    for d in LSTCalendar(
        *dt_range, latitude=latlng[0], longitude=latlng[1], observations=OBSERVATIONS
    ).dates:
        observations = [o.observation.id for o in d.observable_observations()]
        assert sorted(observations) == sorted(expected)
