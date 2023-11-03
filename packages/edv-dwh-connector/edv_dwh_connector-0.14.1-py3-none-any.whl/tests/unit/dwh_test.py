"""
Test case for Date and Time PK.
.. since: 0.5
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

from datetime import date, time, datetime
from dateutil import tz  # type: ignore
from hamcrest import assert_that, equal_to

from edv_dwh_connector.dwh import DatePK, TimePK, DatetimeFromPK


def test_gets_pk_from_date() -> None:
    """
    Should get pk from a date.
    """
    assert_that(
        DatePK(date(2022, 1, 1)).value(), equal_to(20220101)
    )


def test_gets_pk_from_time() -> None:
    """
    Should get pk from a time.
    """
    assert_that(
        TimePK(time(8, 10, 1)).value(), equal_to(81001)
    )


def test_gets_datetime_from_pk() -> None:
    """
    Should get datetime from pk.
    """
    assert_that(
        DatetimeFromPK(20221007, 81001).value(),
        equal_to(datetime(2022, 10, 7, 8, 10, 1, tzinfo=tz.UTC))
    )
