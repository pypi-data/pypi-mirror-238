import pytest
from lstpressure.observation import observable, Observation
from lstpressure.lstindex import LSTIntervalType as I

# 20231030 LST dusk is about 2130


@pytest.mark.parametrize(
    "lst_window_start, lst_window_end, utc_constraints, duration, dt, expected",
    [
        (8, 20, [I.NIGHT_ONLY], 2, "20231030", False),
        (2, 20, [I.NIGHT_ONLY], 0.5, "20231030", True),
        (20, 1, [I.NIGHT_ONLY], 2, "20231030", True),
    ],
)
def test_observable(lst_window_start, lst_window_end, utc_constraints, duration, dt, expected):
    assert (
        observable(
            Observation("~", lst_window_start, lst_window_end, utc_constraints, duration), dt
        )
        is expected
    )
