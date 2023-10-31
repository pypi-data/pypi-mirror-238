import pytest
from lstpressure.lstcalendar import Sun

latitude, longitude = ["-30:42:39.8", "21:26:38.0"]

# NOTE - all times are in UTC


@pytest.mark.parametrize(
    "date, expected_results",
    [
        (
            "20230101",
            {
                "dawn": "2023-01-01 03:06:43.111712",
                "sunrise": "2023-01-01 03:34:52.465661",
                "noon": "2023-01-01 10:37:26.000000",
                "sunset": "2023-01-01 17:40:16.244854",
                "dusk": "2023-01-01 18:08:23.975260",
            },
        ),
        (
            "20230615",
            {
                "dawn": "2023-06-15 05:02:41.873453",
                "sunrise": "2023-06-15 05:29:46.909659",
                "noon": "2023-06-15 10:34:34.000000",
                "sunset": "2023-06-15 15:39:30.356171",
                "dusk": "2023-06-15 16:06:35.427817",
            },
        ),
    ],
)
def test_Sun(date, expected_results):
    sun = Sun(latitude, longitude, date)

    for event, expected_time in expected_results.items():
        calculated_time = getattr(sun, event).strftime("%Y-%m-%d %H:%M:%S.%f")
        assert calculated_time == expected_time
