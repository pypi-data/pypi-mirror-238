"""
lstindex.LSTIndex
------

Contains the Idx class that acts as a wrapper around the IntervalTree class for simplified interval operations.
"""

from intervaltree import IntervalTree, Interval


class LSTIndex:
    """
    A wrapper around the `IntervalTree` class for simplified interval operations.

    This class provides convenience methods to insert and query intervals. It internally uses the `IntervalTree` for interval management and query operations.

    Attributes
    ----------
    idx : IntervalTree
        The internal interval tree used for managing intervals.
    tree : IntervalTree
        Alias for the `idx` attribute.

    Methods
    -------
    get_entries() -> set
        Retrieve all intervals stored in the interval tree.
    insert(*args)
        Insert an interval into the interval tree.
    get_intervals_contained_by(*args) -> set
        Retrieve intervals that are enveloped by the given interval.
    get_intervals_containing(*args) -> list
        Retrieve intervals that contain the given interval.
    """

    def __init__(self):
        """
        Initializes an empty interval tree.
        """
        self.idx = IntervalTree()
        self.tree = self.idx

    def get_entries(self) -> set:
        """
        Retrieve all intervals stored in the interval tree.

        Returns
        -------
        set
            A set of (Interval, data) pairs.
        """
        return self.idx.items()

    def insert(self, *args):
        """
        Insert an interval into the interval tree.

        This method supports multiple calling patterns:
        - With a single Interval argument.
        - With two arguments specifying the start and end of the interval.
        - With three arguments specifying the start, end, and data associated with the interval.

        Parameters
        ----------
        *args
            Variable length argument list.

        Raises
        ------
        ValueError
            If the arguments don't match any of the accepted input patterns.
        """
        if len(args) == 1 and isinstance(args[0], Interval):
            interval = args[0]
            self.idx.add(interval)
        elif len(args) == 2:
            begin, end = args
            self.idx.addi(begin, end, {})
        elif len(args) == 3:
            begin, end, data = args
            self.idx.addi(begin, end, data)
        else:
            raise ValueError("Invalid arguments")

    def get_intervals_contained_by(self, *args) -> set:
        """
        Retrieve intervals that are enveloped by the given interval.

        Parameters
        ----------
        *args
            Variable length argument list.

        Returns
        -------
        set
            A set of intervals enveloped by the provided interval.
        """
        return self.idx.envelop(*args)

    def get_intervals_containing(self, *args) -> list:
        """
        Retrieve intervals that contain the given interval.

        Note
        ----
        The underlying `IntervalTree` doesn't have a direct query for intervals contained
        by some interval. Instead, this method first retrieves all intervals that overlap
        with the query and then filters the results where the query interval is completely
        contained. This approach is efficient.

        Parameters
        ----------
        *args
            Variable length argument list.

        Returns
        -------
        list
            A list of intervals containing the provided interval.
        """

        # Check if the first argument is an instance of Interval
        if isinstance(args[0], Interval):
            query_interval = args[0]
        else:
            query_interval = Interval(*args)

        # Return query results
        return [
            interval
            for interval in self.idx.overlap(*args)
            if interval.contains_interval(query_interval)
        ]
