from ..observation import Observation

default_lat, default_lng = ["-30:42:39.8", "21:26:38.0"]


def observable(
    observation: "Observation", yyyymmdd: str, latitude=default_lat, longitude=default_lng
) -> bool:
    from ..lstcalendar import LSTCalendar

    results = observation.observable(LSTCalendar(yyyymmdd, yyyymmdd, latitude, longitude))
    return bool(len(results))
