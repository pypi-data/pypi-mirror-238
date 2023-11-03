"""
This module defines blend sequences from PostgreSQL.
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

# pylint: disable=duplicate-code
from datetime import date

from sqlalchemy import text  # type: ignore

from edv_dwh_connector.blend_proposal.blend_material import BlendMaterials
from edv_dwh_connector.blend_proposal.blend_sequence import \
    BlendSequence, BlendSequences
from edv_dwh_connector.blend_proposal.db.pg_blend_material \
    import PgBlendMaterials
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import \
    ValueNotFoundError
from edv_dwh_connector.dwh import DatePK


class PgBlendSequence(BlendSequence):
    """
    Blend sequence from PostgreSQL.
    .. since: 0.5
    """

    # pylint: disable=used-before-assignment
    def __init__(self, dte: date, order: int, dwh: Dwh) -> None:
        """
        Ctor.
        :param dte: Date
        :param order: Order
        :param dwh: Dwh
        :raises ValueNotFoundError: If not found
        """
        self.__date = dte
        self.__order = order
        self.__dwh = dwh
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT name "
                    "FROM fact_blend_sequence "
                    "WHERE sequence_pk = :sequence_pk "
                    "and date_pk = :date_pk"
                ),
                (
                    {
                        "sequence_pk": self.__order,
                        "date_pk": DatePK(self.__date).value()
                    }
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("Blend sequence not found")
            self.__name = row["name"]

    def date(self) -> date:
        return self.__date

    def order(self) -> int:
        return self.__order

    def name(self) -> str:
        return self.__name

    def average_au_grade(self) -> float:
        return self.__value_of(BlendSequence.AU_GRADE)

    def soluble_copper(self) -> float:
        return self.__value_of(BlendSequence.SOLUBLE_COPPER)

    def arsenic(self) -> float:
        return self.__value_of(BlendSequence.ARSENIC)

    def moisture_estimated(self) -> float:
        return self.__value_of(BlendSequence.MOISTURE_ESTIMATED)

    def oxide_transition(self) -> float:
        return self.__value_of(BlendSequence.OXIDE_TRANSITION)

    def fresh(self) -> float:
        return self.__value_of(BlendSequence.FRESH)

    def recovery_blend_estimated(self) -> float:
        return self.__value_of(BlendSequence.RECOVERY_BLEND)

    def materials(self) -> BlendMaterials:
        return PgBlendMaterials(self.__date, self.__order, self.__dwh)

    def __value_of(self, name: str) -> float:
        """
        Gets value of characteristic.
        :param name: Characteristic name
        :return: Value
        """
        with self.__dwh.connection() as conn:
            value, = conn.execute(
                # pylint: disable=line-too-long
                text(
                    "SELECT fbm.value "
                    "FROM dim_date dd,dim_blend_charac dbc, dim_sequence ds, fact_blend_measure fbm "  # noqa: E501
                    "WHERE fbm.date_pk = dd.date_pk "
                    "AND fbm.sequence_pk = ds.sequence_pk "
                    "AND fbm.blendcharac_pk = dbc.blendcharac_pk "
                    "AND dbc.name = :name AND fbm.date_pk = :date_pk AND fbm.sequence_pk = :order"  # noqa: E501
                ),
                (
                    {
                        "name": name,
                        "date_pk": DatePK(self.__date).value(),
                        "order": self.__order
                    }
                )
            ).fetchone()
            return float(value)


class PgBlendSequences(BlendSequences):
    """
    Blend sequences from PostgreSQL.
    .. since: 0.5
    """

    def __init__(self, dte: date, dwh: Dwh) -> None:
        """
        Ctor.
        :param dte: Date
        :param dwh: Data warehouse
        """
        self.__date = dte
        self.__dwh = dwh

    def items(self) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT sequence_pk "
                    "FROM fact_blend_sequence "
                    "WHERE date_pk = :date_pk"
                ),
                (
                    {
                        "date_pk": DatePK(self.__date).value()
                    }
                )
            ).fetchall():
                result.append(
                    PgBlendSequence(self.__date, row[0], self.__dwh)
                )
        return result

    def add(self, sequence: BlendSequence) -> BlendSequence:
        if self.has(sequence.name()):
            seq = self.get(sequence.name())
        else:
            date_pk = DatePK(self.__date).value()
            order = sequence.order()
            with self.__dwh.connection() as conn:
                conn.execute(
                    text(
                        "INSERT INTO fact_blend_sequence "
                        "(date_pk, sequence_pk, name) "
                        "VALUES"
                        "(:date_pk, :sequence_pk, :name) "
                    ),
                    (
                        {
                            "date_pk": date_pk,
                            "sequence_pk": order,
                            "name": sequence.name()
                        }
                    )
                )
                seq = PgBlendSequence(
                    self.__date, order, self.__dwh
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.AU_GRADE,
                    value=sequence.average_au_grade()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.SOLUBLE_COPPER,
                    value=sequence.soluble_copper()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.ARSENIC,
                    value=sequence.arsenic()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.MOISTURE_ESTIMATED,
                    value=sequence.moisture_estimated()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.OXIDE_TRANSITION,
                    value=sequence.oxide_transition()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.FRESH,
                    value=sequence.fresh()
                )
                self.__register_measure(
                    date_pk=date_pk, sequence_pk=seq.order(),
                    name=BlendSequence.RECOVERY_BLEND,
                    value=sequence.recovery_blend_estimated()
                )
        for mat in sequence.materials().items():
            seq.materials().add(mat)
        return seq

    def __get_dim_blend_charac_uid(self, name: str) -> int:
        """
        Gets a blend characteristic.
        :param name: Name
        :return: Key
        :raises ValueNotFoundError: If not found
        """
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT blendcharac_pk "
                    "FROM dim_blend_charac "
                    "WHERE name = :name"
                ),
                (
                    {"name": name}
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError(
                    f"Blend characteristic {name} not found"
                )
            return row["blendcharac_pk"]

    def __register_measure(
        self, date_pk: int, sequence_pk: int, name: str, value: float
    ) -> None:
        """
        Registers measure.
        :param date_pk: Date PK
        :param sequence_pk: Sequence PK
        :param name: Characteristic name
        :param value: Value
        """
        charac_pk = self.__get_dim_blend_charac_uid(name)
        with self.__dwh.connection() as conn:
            conn.execute(
                text(
                    "INSERT INTO fact_blend_measure( "
                    "date_pk, sequence_pk, blendcharac_pk, value) "
                    "VALUES(:date_pk, :sequence_pk, :blendcharac_pk, :value) "
                ),
                (
                    {
                        "date_pk": date_pk,
                        "sequence_pk": sequence_pk,
                        "blendcharac_pk": charac_pk,
                        "value": value
                    }
                )
            )
