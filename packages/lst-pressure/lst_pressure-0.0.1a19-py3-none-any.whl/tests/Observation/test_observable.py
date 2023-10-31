from lstpressure.observation import observable, Observation
from lstpressure.lstindex import LSTIntervalType as I

# 20231030 LST is about 2130


def test_observable():
    assert observable(Observation("id", 8, 20, [I.NIGHT_ONLY], 2), "20231030") is False
    assert observable(Observation("id", 2, 20, [I.NIGHT_ONLY], 0.5), "20231030") is True
    assert observable(Observation("id", 20, 1, [I.NIGHT_ONLY], 0.5), "20231030") is True
