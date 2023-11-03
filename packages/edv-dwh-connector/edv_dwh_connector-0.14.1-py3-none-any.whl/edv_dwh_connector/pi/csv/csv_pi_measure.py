"""
This module implements PI measures stored in CSV file.
.. since: 0.13
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
import os

import pandas as pd  # type: ignore

from edv_dwh_connector.pi.pi_measure import PIMeasuresDf


class CsvWithLatestPIMeasuresDf(PIMeasuresDf):
    """
    PI measures that update CSV file with latest data.
    .. since: 0.13
    """

    def __init__(self, path: str, tag, origin: PIMeasuresDf):
        """
        Ctor.
        :param path: CSV file path
        :param tag: PITag or tag code
        :param origin: PIMeasuresDf decorated
        """
        self.__path = path
        if isinstance(tag, str):
            self.__tag = tag
        else:
            self.__tag = tag.code()
        self.__origin = origin

    def frame(self, start: datetime, end: datetime) -> pd.DataFrame:
        last = max(
            PIMeasuresDf.load(self.__path, self.__tag)[
                PIMeasuresDf.DATE_TIME
            ]
        )
        if last is None:
            rstart = start
        else:
            rstart = last.replace(tzinfo=None)
        if rstart <= end:
            self.__origin.frame(rstart, end).to_csv(
                self.__path, mode='a', index=False,
                columns=[PIMeasuresDf.DATE_TIME, PIMeasuresDf.VALUE],
                header=not os.path.exists(self.__path)
            )
        return PIMeasuresDf.load(self.__path, self.__tag)
