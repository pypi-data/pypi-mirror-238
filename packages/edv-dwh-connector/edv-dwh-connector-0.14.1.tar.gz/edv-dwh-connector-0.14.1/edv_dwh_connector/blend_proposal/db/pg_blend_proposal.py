"""
This module defines blend proposals from PostgreSQL.
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

# pylint: disable=unused-import
from datetime import date
import logging

from sqlalchemy import text  # type: ignore

from edv_dwh_connector.blend_proposal.blend_proposal import BlendProposal, \
    BlendProposals
from edv_dwh_connector.blend_proposal.blend_sequence import BlendSequences
from edv_dwh_connector.blend_proposal.db.pg_blend_sequence \
    import PgBlendSequences
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import ValueNotFoundError


class PgBlendProposal(BlendProposal):
    """
    Blend proposal from PostgreSQL.
    .. since: 0.5
    """

    # pylint: disable=used-before-assignment
    def __init__(self, dte: date, dwh: Dwh) -> None:
        """
        Ctor.
        :param dte: Date
        :param dwh: Date warehouse
        """
        self.__date = dte
        self.__dwh = dwh

    def date(self) -> date:
        return self.__date

    def sequences(self) -> BlendSequences:
        return PgBlendSequences(self.__date, self.__dwh)


class PgBlendProposals(BlendProposals):
    """
    Blend proposals from PostgreSQL.
    .. since: 0.5
    """

    def __init__(self, dwh: Dwh):
        self.__dwh = dwh

    def last(self) -> BlendProposal:
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT full_date FROM v_blend_proposal "
                    "ORDER BY full_date DESC "
                    "LIMIT 1"
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError(
                    "Unable to find last blend proposal: list is empty"
                )
            return PgBlendProposal(row[0], self.__dwh)

    def has_at(self, dte: date) -> bool:
        with self.__dwh.connection() as conn:
            count, = conn.execute(
                text(
                    "SELECT count(*) FROM v_blend_proposal "
                    "WHERE full_date = :date "
                ),
                (
                    {
                        "date": dte
                    }
                )
            ).fetchone()
            return count > 0

    def get_at(self, dte: date) -> BlendProposal:
        if self.has_at(dte):
            return PgBlendProposal(dte, self.__dwh)
        raise ValueNotFoundError(
            f"Blend proposal not found at date {dte.strftime('%Y-%m-%d')}"
        )

    # pylint: disable=duplicate-code
    def items(self, start: date = None, end: date = None) -> list:
        if start is None or end is None:
            raise ValueError(
                "You must specify start and end date for "
                "blend proposals coming from the database"
            )
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT full_date FROM v_blend_proposal "
                    "WHERE full_date BETWEEN :start AND :end "
                    "ORDER BY full_date DESC "
                ),
                (
                    {
                        "start": start,
                        "end": end
                    }
                )
            ).fetchall():
                result.append(
                    PgBlendProposal(row[0], self.__dwh)
                )
        return result

    def add(self, blend: BlendProposal) -> BlendProposal:
        logging.info(
            "Adding blend proposal of %s: %s sequence(s)",
            blend.date(), len(blend.sequences().items())
        )
        if len(blend.sequences().items()) == 0:
            raise ValueError("Blend proposal to add has no sequence")

        try:
            # pylint: disable=unused-variable
            with self.__dwh.begin() as trx:  # noqa: F841
                item = PgBlendProposal(blend.date(), self.__dwh)
                for seq in blend.sequences().items():
                    item.sequences().add(seq)
                return item
        finally:
            self.__dwh.terminate()
