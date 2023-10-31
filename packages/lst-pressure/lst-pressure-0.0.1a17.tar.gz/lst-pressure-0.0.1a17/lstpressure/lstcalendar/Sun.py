"""
lstcalendar.Sun
"""
from typing import Union
from astral.sun import sun as calc_sun
from astral import LocationInfo
from ..utils import normalize_coordinates, normalize_yyyymmdd_to_datetime, utc_to_lst


class Sun:
    """
    Sun statistics for a particular date, at a particular lat/long.

    :ivar dawn: The dawn time (datetime object) for the given date and location.
    :ivar sunrise: The sunrise time (datetime object) for the given date and location.
    :ivar noon: The solar noon time (datetime object) for the given date and location.
    :ivar sunset: The sunset time (datetime object) for the given date and location.
    :ivar dusk: The dusk time (datetime object) for the given date and location.
    """

    def __init__(
        self, latitude: Union[float, str], longitude: Union[float, str], yyyymmdd: str
    ) -> None:
        latitude, longitude = normalize_coordinates(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
        dt = normalize_yyyymmdd_to_datetime(yyyymmdd)
        location = LocationInfo(latitude=latitude, longitude=longitude)
        location.timezone = "UTC"
        self._attributes = calc_sun(location.observer, date=dt)

    @property
    def dawn(self):
        return self._attributes.get("dawn")

    @property
    def dawn_lst(self):
        return utc_to_lst(self._attributes.get("dawn"), self.latitude, self.longitude)

    @property
    def sunrise(self):
        return self._attributes.get("sunrise")

    @property
    def sunrise_lst(self):
        return utc_to_lst(self._attributes.get("sunrise"), self.latitude, self.longitude)

    @property
    def noon(self):
        return self._attributes.get("noon")

    @property
    def noon_lst(self):
        return utc_to_lst(self._attributes.get("noon"), self.latitude, self.longitude)

    @property
    def sunset(self):
        return self._attributes.get("sunset")

    @property
    def sunset_lst(self):
        return utc_to_lst(self._attributes.get("sunset"), self.latitude, self.longitude)

    @property
    def dusk(self):
        return self._attributes.get("dusk")

    @property
    def dusk_lst(self):
        return utc_to_lst(self._attributes.get("dusk"), self.latitude, self.longitude)
