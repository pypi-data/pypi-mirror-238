"""
This module defines Excel sequence total row.
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

import re
from openpyxl.worksheet.worksheet import Worksheet  # type: ignore

from edv_dwh_connector.blend_proposal.excel.start_cell import StartCell


# pylint: disable=too-few-public-methods
class SequenceTotalRow:
    """
    Total number of rows of a sequence table.
    .. since: 0.5
    """

    def __init__(self, sheet: Worksheet, bs_start_cell: StartCell) -> None:
        """
        Ctor.
        :param sheet: Worksheet
        :param bs_start_cell: Blend sequence start cell
        """
        self.__sheet = sheet
        self.__bs_start_cell = bs_start_cell

    def count(self) -> int:
        """
        Gets count.
        :return: Count
        """
        number = 1
        row = self.__bs_start_cell.row()
        while row < self.__bs_start_cell.row() + 100:
            number = number + 1
            row = row + 1
            col = -1
            for i in range(1, 5):
                if self.__sheet.cell(
                    row, self.__bs_start_cell.column() - i
                ).value is not None:
                    col = self.__bs_start_cell.column() - i
                    break
            if col > -1 and re.search(
                "recovery", self.__sheet.cell(row, col).value, re.IGNORECASE
            ):
                break
        return number
