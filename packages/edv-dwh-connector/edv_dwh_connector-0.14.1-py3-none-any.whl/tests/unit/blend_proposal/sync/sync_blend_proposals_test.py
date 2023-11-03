"""
Test case for synchronized blend proposals.
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

from datetime import date
from hamcrest import assert_that, equal_to
from edv_dwh_connector.blend_proposal.sync.sync_blend_proposals\
    import SyncBlendProposals
from edv_dwh_connector.blend_proposal.excel.excel_blend_proposal \
    import ExcelBlendProposals
from edv_dwh_connector.blend_proposal.blend_proposal\
    import LocalBlendProposals


EXCEL_BLEND_FILE = "3.Daily_Blend_Template_process_October.xlsx"


def test_synchronizes(resource_path_root) -> None:
    """
    Test that it synchronizes.
    :param resource_path_root: Resource path
    """
    src = ExcelBlendProposals(
        file=resource_path_root / EXCEL_BLEND_FILE,
        start_date=date.fromisoformat("2022-10-18"),
        end_date=date.fromisoformat("2022-10-20")
    )
    assert_that(
        len(src.items()), equal_to(3),
        "Source blend proposals length should match"
    )
    sync = SyncBlendProposals(src, LocalBlendProposals())
    sync.synchronize()
    items = sync.items()
    assert_that(
        len(items), equal_to(3),
        "Target blend proposals should synchronize"
    )
    assert_that(
        items[0].date(),
        equal_to(date.fromisoformat("2022-10-18")),
        "Blend proposal 1 date should match"
    )
    assert_that(
        items[1].date(),
        equal_to(date.fromisoformat("2022-10-19")),
        "Blend proposal 2 date should match"
    )
    assert_that(
        sync.last().date(),
        equal_to(date.fromisoformat("2022-10-20")),
        "Blend proposal 3 date should match"
    )
