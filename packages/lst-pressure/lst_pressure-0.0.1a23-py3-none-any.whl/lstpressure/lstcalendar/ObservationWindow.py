from ..observation import Observation
from ..lstindex import LSTInterval


class ObservationWindow:
    """
    Represents a valid scheduling time frame based on observational constraints.

    Attributes:
        interval (Any): The time interval or range representing the observation window.
        observation (Any): The observational data or constraints defining the validity of the interval.
    """

    def __init__(self, interval: "LSTInterval", observation):
        """
        Initializes an instance of the ObservationWindow class.

        :param interval: The time interval or range for the observation window.
        :type interval: Any
        :param observation: The observational constraints or data associated with the interval.
        :type observation: Any
        """
        self._interval = interval
        self._observation = observation

    @property
    def interval(self) -> "LSTInterval":
        return self._interval

    @property
    def observation(self) -> "Observation":
        return self._observation

    def __str__(self):
        """
        Returns a string representation of the ObservationWindow.

        :return: A string describing the observation window.
        :rtype: str
        """
        return f"ObservationWindow(interval={self.interval}, observation={self.observation})"
