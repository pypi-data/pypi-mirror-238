"""
Test case for ExcelBlendProposals.
.. since: 0.1
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

from datetime import date
from hamcrest import assert_that, equal_to
from edv_dwh_connector.blend_proposal.excel.excel_blend_proposal \
    import ExcelBlendProposals

BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_blends(resource_path_root) -> None:
    """
    Tests that it gets blends.
    :param resource_path_root: Resource path
    """

    blends = ExcelBlendProposals(
        file=resource_path_root / BLEND_FILE_NAME,
        start_date=date.fromisoformat("2022-10-15"),
        end_date=date.fromisoformat("2022-10-17")
    )
    items = blends.items()
    assert_that(
        len(items),
        equal_to(3),
        "Blend proposal items count should match"
    )
    assert_that(
        items[0].date(),
        equal_to(date.fromisoformat("2022-10-15")),
        "Blend proposal 1 data should match"
    )
    assert_that(
        items[1].date(),
        equal_to(date.fromisoformat("2022-10-16")),
        "Blend proposal 2 data should match"
    )
    assert_that(
        blends.last().date(),
        equal_to(date.fromisoformat("2022-10-17")),
        "Blend proposal 3 data should be the last"
    )
