"""
This module defines Excel blend proposal.
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

from datetime import date, timedelta, datetime
import logging
import openpyxl  # type: ignore
from openpyxl.worksheet.worksheet import Worksheet  # type: ignore
from edv_dwh_connector.blend_proposal.blend_proposal import BlendProposal,\
    BlendProposals
from edv_dwh_connector.blend_proposal.blend_sequence import BlendSequences
from edv_dwh_connector.blend_proposal.excel.excel_blend_sequence \
    import ExcelBlendSequences
from edv_dwh_connector.blend_proposal.excel.start_cell \
    import StartCell
from edv_dwh_connector.blend_proposal.excel.blend_proposal_start_cell \
    import BlendProposalStartCell
from edv_dwh_connector.exceptions import ValueNotFoundError


class ExcelBlendProposal(BlendProposal):
    """
    Excel blend proposal.
    .. since: 0.1
    """

    def __init__(self, sheet: Worksheet, bp_start_cell: StartCell) -> None:
        """
        Ctor.
        :param sheet: Worksheet
        :param bp_start_cell: Blend proposal start cell
        """
        self.__sheet = sheet
        self.__bp_start_cell = bp_start_cell

    def date(self) -> date:
        return self.__sheet.cell(
            self.__bp_start_cell.row(), self.__bp_start_cell.column() + 1
        ).value.date()

    def sequences(self) -> BlendSequences:
        return ExcelBlendSequences(
            sheet=self.__sheet, bp_start_cell=self.__bp_start_cell
        )


class ExcelBlendProposals(BlendProposals):
    """
    Blend proposals from Excel file.
    """

    def __init__(self, file: str, start_date: date, end_date: date) -> None:
        """
        Ctor.
        :param file: Path of Excel file
        :param start_date: Start date
        :param end_date: End date
        """
        self.__file = file
        self.__start_date = start_date.date()\
            if isinstance(start_date, datetime) else start_date
        self.__end_date = end_date.date() if isinstance(end_date, datetime)\
            else end_date
        self.__blends = []  # type: ignore

    def last(self) -> BlendProposal:
        size = len(self.__blends)
        if size == 0:
            raise ValueNotFoundError(
                "Unable to find last blend proposal: list is empty"
            )
        return self.__blends[size - 1]

    def add(self, blend: BlendProposal) -> BlendProposal:
        raise NotImplementedError(
            "Adding blend proposal to an Excel file is not supported"
        )

    def items(self, start: date = None, end: date = None) -> list:
        if len(self.__blends) == 0:
            logging.info("Loading blend proposal excel file %s", self.__file)
            book = openpyxl.load_workbook(self.__file, data_only=True)
            delta = self.__end_date - self.__start_date
            for day in range(0, delta.days + 1):
                bps = BlendProposalStartCell(
                    sheet=book.active,
                    day=self.__start_date + timedelta(days=day)
                )
                if bps.exist():
                    self.__blends.append(
                        ExcelBlendProposal(
                            sheet=book.active, bp_start_cell=bps
                        )
                    )
            logging.info(
                "Found %s blends from %s to %s", len(self.__blends),
                self.__start_date, self.__end_date
            )
        if start is None or end is None:
            blends = self.__blends
        else:
            blends = []
            for blend in self.__blends:
                if start <= blend.date() <= end:
                    blends.append(blend)
        return blends
