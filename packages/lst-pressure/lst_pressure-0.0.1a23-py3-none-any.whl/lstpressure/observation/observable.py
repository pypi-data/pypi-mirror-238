from ..observation import Observation
from ..lstcalendar import LSTCalendar
from typing import Optional


def observable(
    observation: "Observation",
    yyyymmdd_start: Optional[str] = None,
    yyyymmdd_end: Optional[str] = None,
    lstCalendar: Optional["LSTCalendar"] = None,
    latitude: Optional[str] = "-30:42:39.8",
    longitude: Optional[str] = "21:26:38.0",
) -> bool:
    """
    Determines if an observation is observable within the specified date and location parameters.

    :param observation: The Observation object to be checked.
    :type observation: Observation
    :param yyyymmdd_start: (Optional) The start date in the format 'YYYYMMDD'.
    :type yyyymmdd_start: Optional[str]
    :param yyyymmdd_end: (Optional) The end date in the format 'YYYYMMDD'. If not provided, the start date is used.
    :type yyyymmdd_end: Optional[str]
    :param lstCalendar: (Optional) An instance of LSTCalendar. If not provided, a new LSTCalendar instance will be created based on the date and location parameters.
    :type lstCalendar: Optional[LSTCalendar]
    :param latitude: (Optional) The latitude for the observation in the format 'D:M:S'. Default is "-30:42:39.8".
    :type latitude: Optional[str]
    :param longitude: (Optional) The longitude for the observation in the format 'D:M:S'. Default is "21:26:38.0".
    :type longitude: Optional[str]
    :return: True if the observation is observable within the specified parameters, False otherwise.
    :rtype: bool
    """

    from ..lstcalendar import LSTCalendar

    yyyymmdd_end = yyyymmdd_end if yyyymmdd_end else yyyymmdd_start
    calendar = (
        lstCalendar
        if lstCalendar
        else LSTCalendar(yyyymmdd_start, yyyymmdd_end, latitude, longitude)
    )

    results = observation.observable_dates(calendar)
    return bool(len(results))
