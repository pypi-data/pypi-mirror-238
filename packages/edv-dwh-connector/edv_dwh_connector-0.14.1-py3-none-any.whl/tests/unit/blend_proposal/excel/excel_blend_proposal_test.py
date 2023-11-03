"""
Test case for ExcelBlendProposal.
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
import openpyxl  # type: ignore
from hamcrest import assert_that, equal_to

from tests.unit.blend_proposal.excel.fake_start_cell import FakeStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_proposal \
    import ExcelBlendProposal, ExcelBlendProposals

BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_a_blend(resource_path_root) -> None:
    """
    Tests that it gets a blend.
    :param resource_path_root: Resource path
    """

    blend = ExcelBlendProposal(
        sheet=openpyxl.load_workbook(
            resource_path_root / BLEND_FILE_NAME
        ).active,
        bp_start_cell=FakeStartCell(row=7, column=6)
    )
    assert_that(
        blend.date(),
        equal_to(date(2022, 10, 7)),
        "Blend proposal date should match"
    )
    assert_that(
        len(blend.sequences().items()),
        equal_to(3),
        "Blend proposal sequences count should match"
    )


def test_reads_a_blend_with_formula_cell(resource_path_root) -> None:
    """
    Tests that it reads a blend with a formula cell.
    :param resource_path_root: Resource path
    """
    dte = date(2022, 11, 9)
    blend = ExcelBlendProposals(
        resource_path_root / "blend_proposal_with_formula.xlsx",
        dte, dte
    ).get_at(dte)
    assert_that(
        blend.date(), equal_to(dte),
        "Blend proposal date should match"
    )
    seq = blend.sequences().items()[2]
    assert_that(
        seq.name(), equal_to("IF LEP_LG_FR IS FINISHED"),
        "Sequence name should match"
    )
    assert_that(
        seq.average_au_grade(), equal_to(1.6676214629507886),
        "Average Au grade Formula cell should be calculated"
    )
    assert_that(
        seq.materials().items()[0].proportion(), equal_to(0.08571428569384752),
        "Prop Formula cell should be calculated"
    )
