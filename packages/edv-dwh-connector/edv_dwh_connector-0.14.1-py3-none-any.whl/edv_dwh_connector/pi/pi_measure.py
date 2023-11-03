"""
This module defines PI measure API.
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
from typing import Final

from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd  # type: ignore

from edv_dwh_connector.pi.pi_tag import PITag


class PIMeasure(ABC):
    """
    Measure of a PI tag.
    .. since: 0.2
    """

    @abstractmethod
    def date(self) -> datetime:
        """
        Gets date.
        :return: Datetime
        """

    @abstractmethod
    def tag(self) -> PITag:
        """
        Gets Tag.
        :return: Tag
        """

    @abstractmethod
    def value(self) -> float:
        """
        Gets value.
        :return: Value
        """


class PIMeasures(ABC):
    """
    Set of measures for a PI tag.
    .. since: 0.2
    """

    @abstractmethod
    def has_at(self, date: datetime) -> bool:
        """
        Checks that has measure at date.
        :param date: Date
        :return: Has data at date or not
        """

    @abstractmethod
    def last(self) -> PIMeasure:
        """
        Gets last PI measure.
        :return: Last measure
        :raises ValueNotFoundError: If there isn't a measure
        """

    @abstractmethod
    def items(self, start: datetime, end: datetime) -> list:
        """
        Gets all measures on period
        :param start: Start date
        :param end: End date
        :return: List of tags
        """

    @abstractmethod
    def add(self, date: datetime, value: float) -> PIMeasure:
        """
        Adds a new measure.
        :param date: Datetime
        :param value: Value
        :return: Measure registered
        :raises ValueAlreadyExistsError: If a measure of the tag already
            exists at the same datetime
        """


# pylint: disable=too-few-public-methods
class PIMeasuresDf(ABC):
    """
    PI Measure working with Data frame.
    .. since: 0.9
    """

    DATE_TIME: Final[str] = "DateTime"

    NAME: Final[str] = "Name"

    VALUE: Final[str] = "Value"

    @staticmethod
    def load(file, code) -> pd.DataFrame:
        """
        Loads data from CSV file
        :param file: CSV file
        :param code: Tag code
        :return: DataFrame
        """
        dtf = pd.read_csv(
            file,
            parse_dates=[PIMeasuresDf.DATE_TIME],
            names=[
                PIMeasuresDf.DATE_TIME, PIMeasuresDf.VALUE
            ],
            header=0
        )
        dtf[PIMeasuresDf.NAME] = code
        return dtf

    @abstractmethod
    def frame(self, start: datetime, end: datetime) -> pd.DataFrame:
        """
        Gets data frame.
        :param start: Start date
        :param end: End date
        :return: DataFrame
        """
