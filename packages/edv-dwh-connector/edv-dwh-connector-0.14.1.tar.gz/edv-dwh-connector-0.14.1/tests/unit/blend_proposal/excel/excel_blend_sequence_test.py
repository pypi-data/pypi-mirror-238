"""
Test case for Excel blend sequence.
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
from hamcrest import assert_that, equal_to, has_length, contains_inanyorder
from edv_dwh_connector.blend_proposal.excel.blend_proposal_start_cell \
    import BlendProposalStartCell
from edv_dwh_connector.blend_proposal.excel.blend_sequence_start_cell \
    import BlendSequenceStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_sequence \
    import ExcelBlendSequence


BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_a_sequence(resource_path_root) -> None:
    """
    Tests that it gets a sequence.
    :param resource_path_root: Resource path
    """

    sheet = openpyxl.load_workbook(
        resource_path_root / BLEND_FILE_NAME
    ).active
    bps = BlendProposalStartCell(
        sheet=sheet, day=date(2022, 10, 7)
    )
    start = BlendSequenceStartCell(
        sheet=sheet,
        bp_start_cell=bps,
        number=2
    )
    sequence = ExcelBlendSequence(
        sheet=sheet, order=2, bp_start_cell=bps, bs_start_cell=start
    )
    assert_that(
        sequence.order(), equal_to(2),
        "Sequence order should match"
    )
    assert_that(
        sequence.name(),
        equal_to("IF LEP_HG_FR_LCU  IS  FINISHED"),
        "Sequence name should match"
    )
    assert_that(
        sequence.average_au_grade(),
        equal_to(2.1455512539376826),
        "Sequence average grade should match"
    )
    assert_that(
        sequence.soluble_copper(),
        equal_to(523.8789666535029),
        "Sequence soluble copper should match"
    )
    assert_that(
        sequence.arsenic(),
        equal_to(775.6473173467315),
        "Sequence As should match"
    )
    assert_that(
        sequence.moisture_estimated(),
        equal_to(0.17179342384894572),
        "Sequence moisture estimated should match"
    )
    assert_that(
        sequence.oxide_transition(),
        equal_to(0.5754824872105082),
        "Sequence oxide/transition should match"
    )
    assert_that(
        sequence.fresh(),
        equal_to(0.42451751278949185),
        "Sequence fresh should match"
    )
    assert_that(
        sequence.recovery_blend_estimated(),
        equal_to(0.7699378617990029),
        "Sequence recovery blend estimated should match"
    )
    assert_that(
        sequence.materials().items(),
        has_length(6),
        "Sequence material count should match"
    )
    assert_that(
        [material.name() for material in sequence.materials().items()],
        contains_inanyorder(
            "VSM_LG_HG_AS", "LG_HG_OX_TR_HCU", "LG_OX_TR_LCU", "LEP_HG_FR_LCU",
            "SURGE_BIN_OX_LG_HG", "SURGE_BIN_FR_LG_HG"
        ),
        "Sequence materials names should match"
    )
