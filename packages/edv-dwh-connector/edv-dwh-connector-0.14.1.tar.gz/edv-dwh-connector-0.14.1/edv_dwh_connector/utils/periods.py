"""
This module defines Periods.
.. since: 0.2
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# pylint: disable=too-few-public-methods


class Period(ABC):
    """
    Period.
    .. since: 0.3
    """

    @abstractmethod
    def start(self) -> datetime:
        """
        Gets start date.
        :return: Datetime
        """

    @abstractmethod
    def end(self) -> datetime:
        """
        Gets end date.
        :return: Datetime
        """


class Periods(ABC):
    """
    Multiple periods
    .. since: 0.3
    """

    @abstractmethod
    def items(self) -> list:
        """
        Get all intervals on the period
        :return: List of intervals
        """


class SingleInPeriods(Periods):
    """
    Single period in the list.
    .. since: 0.3
    """

    def __init__(self, start: datetime, end: datetime) -> None:
        """
        Ctor.
        :param start: Start date
        :param end: End date
        """
        self.__start = start
        self.__end = end

    def items(self) -> list:
        return [SimplePeriod(self.__start, self.__end)]


class SimplePeriod(Period):
    """
    Simple period.
    .. since: 0.3
    """

    def __init__(self, start: datetime, end: datetime):
        """
        Ctor.
        :param start: Start date
        :param end: End date
        """
        self.__start = start
        self.__end = end

    def start(self) -> datetime:
        return self.__start

    def end(self) -> datetime:
        return self.__end


class DayIntervals(Periods):
    """
    Split period in day intervals.
    .. since: 0.3
    """

    def __init__(self, start: datetime, end: datetime):
        """
        Ctor.
        :param start: Start date
        :param end: End date
        :raises ValueError: If start and end dates are wrong
        """
        if start > end:
            raise ValueError(
                "Bad range, dates are equals "
                "or start date is greater than end date"
            )
        self.__start = start
        self.__end = end

    def items(self) -> list:
        periods = []
        nbr_of_seconds = 3600 * 24
        total_seconds_from_two_date = (self.__end - self.__start)\
            .total_seconds()
        if total_seconds_from_two_date <= nbr_of_seconds:
            periods.append(SimplePeriod(self.__start, self.__end))
        else:
            total_nbr_days = total_seconds_from_two_date / nbr_of_seconds
            if total_nbr_days - int(total_nbr_days) == 0.0:
                total_nbr_days = int(total_nbr_days)
            else:
                total_nbr_days = int(total_nbr_days) + 1
            for day in range(0, total_nbr_days):
                start = self.__start + timedelta(days=day)
                if day < total_nbr_days - 1:
                    periods.append(
                        SimplePeriod(
                            start, start + timedelta(days=1, seconds=-1)
                        )
                    )
                elif day == total_nbr_days - 1:
                    periods.append(
                        SimplePeriod(start, self.__end)
                    )
        return periods


class HourIntervals(Periods):
    """
    Split period in hour intervals.
    .. since: 0.6
    """

    def __init__(self, start: datetime, end: datetime):
        """
        Ctor.
        :param start: Start date
        :param end: End date
        :raises ValueError: If start and end dates are wrong
        """
        if start > end:
            raise ValueError(
                "Bad range, dates are equals "
                "or start date is greater than end date"
            )
        self.__start = start
        self.__end = end

    def items(self) -> list:
        periods = []
        nbr_of_seconds = 3600
        total_seconds_from_two_date = (self.__end - self.__start)\
            .total_seconds()
        if total_seconds_from_two_date <= nbr_of_seconds:
            periods.append(SimplePeriod(self.__start, self.__end))
        else:
            total_hours = total_seconds_from_two_date / nbr_of_seconds
            if total_hours - int(total_hours) == 0.0:
                total_hours = int(total_hours)
            else:
                total_hours = int(total_hours) + 1
            for hour in range(0, total_hours):
                start = self.__start + timedelta(hours=hour)
                if hour < total_hours - 1:
                    periods.append(
                        SimplePeriod(
                            start, start + timedelta(hours=1, seconds=-1)
                        )
                    )
                elif hour == total_hours - 1:
                    periods.append(
                        SimplePeriod(start, self.__end)
                    )
        return periods
