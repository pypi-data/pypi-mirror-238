"""
Test case for ExcelSequenceMaterial.
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
from hamcrest import assert_that, equal_to, is_,\
    has_length, contains_inanyorder
from edv_dwh_connector.blend_proposal.excel.blend_proposal_start_cell \
    import BlendProposalStartCell
from edv_dwh_connector.blend_proposal.excel.blend_sequence_start_cell \
    import BlendSequenceStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_material \
    import ExcelBlendMaterial, ExcelBlendMaterials
from edv_dwh_connector.blend_proposal.excel.blend_material_start_cell \
    import BlendMaterialStartCell


BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_a_material(resource_path_root) -> None:
    """
    Tests that it gets a material.
    :param resource_path_root: Resource path
    """
    sheet = openpyxl.load_workbook(
        resource_path_root / BLEND_FILE_NAME
    ).active
    bs_start = BlendSequenceStartCell(
        sheet=sheet,
        bp_start_cell=BlendProposalStartCell(
            sheet=sheet, day=date(2022, 10, 7)
        ),
        number=1
    )
    sm_start = BlendMaterialStartCell(row=17, column=9)
    material = ExcelBlendMaterial(
        sheet=sheet, bs_start_cell=bs_start, sm_start_cell=sm_start
    )
    assert_that(
        material.name(),
        equal_to("SURGE_BIN_OX_LG_HG"),
        "Material name should match"
    )
    assert_that(
        material.machine(),
        equal_to("SURGE BIN"),
        "Material type should match"
    )
    assert_that(
        material.pit(),
        equal_to("LEP/WAL/BAK"),
        "Material pit should match"
    )
    assert_that(
        material.au_grade(),
        equal_to(2.425),
        "Material Au grade should match"
    )
    assert_that(
        material.soluble_copper(),
        equal_to(947),
        "Material sol cu should match"
    )
    assert_that(
        material.arsenic(),
        equal_to(92.991842),
        "Material As should match"
    )
    assert_that(
        material.moisture(),
        equal_to(0.21),
        "Material Moisture should match"
    )
    assert_that(
        material.indicative_rec(),
        equal_to(0.892351),
        "Material Indicative rec should match"
    )
    assert_that(
        material.bucket(),
        equal_to(3),
        "Material Bucket should match"
    )
    assert_that(
        material.available_tons(),
        equal_to(5380.98),
        "Material Available tons should match"
    )
    assert_that(
        material.proportion(),
        equal_to(0.2754824872105081),
        "Material Prop should match"
    )


def test_list_materials(resource_path_root) -> None:
    """
    Tests that it lists materials.
    :param resource_path_root: Resource path
    """
    sheet = openpyxl.load_workbook(
        resource_path_root / BLEND_FILE_NAME
    ).active
    materials = ExcelBlendMaterials(
        sheet=sheet,
        bs_start_cell=BlendSequenceStartCell(
            sheet=sheet,
            bp_start_cell=BlendProposalStartCell(
                sheet=sheet, day=date(2022, 10, 7)
            ),
            number=1
        )
    )
    assert_that(
        materials.items(),
        has_length(6),
        "Materials count should match"
    )
    assert_that(
        [material.name() for material in materials.items()],
        contains_inanyorder(
            "VSM_LG_HG_AS", "LG_OX_TR_LCU", "LG_HG_OX_TR_HCU", "LEP_HG_FR_LCU",
            "SURGE_BIN_OX_LG_HG", "SURGE_BIN_FR_LG_HG"
        ),
        "Materials names should match"
    )
    assert_that(
        materials.has("LG_HG_OX_TR_HCU"), is_(True),
        "Materials should contain material with given name"
    )
    assert_that(
        materials.has("LG_HG_OX_TR_HCU2"), is_(False),
        "Materials should not contain material with given name"
    )
    assert_that(
        materials.get("SURGE_BIN_FR_LG_HG").name(),
        equal_to("SURGE_BIN_FR_LG_HG"),
        "Materials should get one by its name"
    )
