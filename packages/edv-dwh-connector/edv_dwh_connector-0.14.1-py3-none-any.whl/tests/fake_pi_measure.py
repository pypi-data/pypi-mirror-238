"""
This module implements a fake PI measures.
.. since: 0.3
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

from datetime import datetime

import pandas as pd  # type: ignore

from edv_dwh_connector.pi.pi_tag import PITag
from edv_dwh_connector.pi.pi_measure import PIMeasure, PIMeasures, PIMeasuresDf
from edv_dwh_connector.pi.cached.cached_pi_measure import CachedPIMeasure
from edv_dwh_connector.exceptions \
    import ValueAlreadyExistsError, ValueNotFoundError


class FakePIMeasures(PIMeasures):
    """
    Fake PI measures.
    .. since: 0.3
    """

    def __init__(self, tag: PITag) -> None:
        """
        Ctor.
        :param tag: Tag
        """
        self.__tag = tag
        self.__measures = []  # type: ignore

    def has_at(self, date: datetime) -> bool:
        clean_date = datetime.strptime(
            date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "%Y-%m-%d %H:%M:%S.%f"
        )
        found = False
        for measure in self.__measures:
            if measure.date() == clean_date:
                found = True
                break
        return found

    def last(self) -> PIMeasure:
        size = len(self.__measures)
        if size == 0:
            raise ValueNotFoundError("Last PI measure not found")
        return self.__measures[size - 1]

    def items(self, start: datetime, end: datetime) -> list:
        measures = []
        for measure in self.__measures:
            if start <= measure.date() <= end:
                measures.append(measure)
        return measures

    def add(self, date: datetime, value: float) -> PIMeasure:
        if self.has_at(date):
            raise ValueAlreadyExistsError(
                "A measure already exists at "
                f"{date} for tag {self.__tag.code()}"
            )
        measure = CachedPIMeasure(self.__tag, date, value)
        self.__measures.append(measure)
        return measure


class FakePIMeasuresDf(PIMeasuresDf):
    """
    Fake PI measures.
    .. since: 0.13
    """

    def __init__(self, measures: PIMeasures):
        """
        Ctor.
        :param measures: Measures
        """
        self.__measures = measures

    def frame(self, start: datetime, end: datetime) -> pd.DataFrame:
        result = dict(  # type: ignore
            DateTime=[],
            Name=[],
            Value=[]
        )
        for mea in self.__measures.items(start, end):
            result[PIMeasuresDf.DATE_TIME].append(mea.date())
            result[PIMeasuresDf.NAME].append(mea.tag().code())
            result[PIMeasuresDf.VALUE].append(mea.value())
        return pd.DataFrame(result)
