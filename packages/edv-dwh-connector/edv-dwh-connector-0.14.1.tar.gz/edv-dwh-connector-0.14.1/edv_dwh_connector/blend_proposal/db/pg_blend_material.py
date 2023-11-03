"""
This module defines blend materials from PostgreSQL.
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

from sqlalchemy import text  # type: ignore

from edv_dwh_connector.blend_proposal.blend_material \
    import BlendMaterial, BlendMaterials
from edv_dwh_connector.dwh import Dwh, DatePK
from edv_dwh_connector.exceptions import ValueNotFoundError


class PgBlendMaterial(BlendMaterial):
    """
    Blend material from PostgreSQL.
    .. since: 0.5
    """

    def __init__(
        self, dte: date, seq_order: int, name: str, dwh: Dwh
    ) -> None:
        """
        Ctor.
        :param dte: Date
        :param seq_order: Sequence order
        :param name: Material name
        :param dwh: Data warehouse
        :raises ValueNotFoundError: If not found
        """
        self.__date = dte
        self.__seq_order = seq_order
        self.__name = name
        self.__dwh = dwh
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT description, "
                    "get_type_machine(name) machine_type "
                    "FROM dim_material "
                    "WHERE name = :name"
                ),
                (
                    {
                        "name": self.__name
                    }
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("Blend material not found")
            self.__machine_type = row["machine_type"]

    def machine(self) -> str:
        return self.__machine_type

    def pit(self) -> str:
        with self.__dwh.connection() as conn:
            value, = conn.execute(
                text(
                    "SELECT pit.name "
                    "FROM fact_material_measure fmm, "
                    "dim_material dm, dim_pit pit  "
                    "WHERE fmm.pit_pk = pit.pit_pk "
                    "and fmm.material_pk = dm.material_pk "
                    "and dm.name = :name "
                    "and fmm.sequence_pk = :sequence_pk "
                    "and fmm.date_pk = :date_pk "
                    "LIMIT 1"
                ),
                (
                    {
                        "name": self.name(),
                        "sequence_pk": self.__seq_order,
                        "date_pk": DatePK(self.__date).value()
                    }
                )
            ).fetchone()
            return value

    def name(self) -> str:
        return self.__name

    def au_grade(self) -> float:
        return self.__value_of(BlendMaterial.AU_GRADE)

    def soluble_copper(self) -> float:
        return self.__value_of(BlendMaterial.SOL_CU)

    def arsenic(self) -> float:
        return self.__value_of(BlendMaterial.ARSENIC)

    def moisture(self) -> float:
        return self.__value_of(BlendMaterial.MOISTURE)

    def indicative_rec(self) -> float:
        return self.__value_of(BlendMaterial.INDICATIVE_REC)

    def bucket(self) -> float:
        return self.__value_of(BlendMaterial.BUCKET)

    def available_tons(self) -> float:
        return self.__value_of(BlendMaterial.AVAILABLE_TONS)

    def proportion(self) -> float:
        return self.__value_of(BlendMaterial.PROP)

    def __value_of(self, name: str) -> float:
        """
        Gets value of material characteristic.
        :param name: Material characteristic
        :return: Value
        """
        with self.__dwh.connection() as conn:
            value, = conn.execute(
                text(
                    "SELECT fmm.value "
                    "FROM fact_material_measure fmm, dim_material dm, "
                    "dim_material_charac dmc  "
                    "WHERE fmm.materialcharac_pk = dmc.materialcharac_pk "
                    "and fmm.material_pk = dm.material_pk "
                    "and fmm.sequence_pk = :sequence_pk "
                    "and fmm.date_pk = :date_pk "
                    "and dm.name = :mat_name "
                    "and dmc.name = :name"
                ),
                (
                    {
                        "sequence_pk": self.__seq_order,
                        "date_pk": DatePK(self.__date).value(),
                        "mat_name": self.__name,
                        "name": name
                    }
                )
            ).fetchone()
            return float(value)


class PgBlendMaterials(BlendMaterials):
    """
    Blend materials from PostgreSQL.
    .. since: 0.5
    """

    def __init__(self, dte: date, seq_order: int, dwh: Dwh) -> None:
        """
        Ctor.
        :param dte: Sequence
        :param seq_order: Sequence order
        :param dwh: Data warehouse
        """
        self.__date = dte
        self.__seq_order = seq_order
        self.__dwh = dwh

    # pylint: disable=duplicate-code
    def items(self) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                    text(
                        "SELECT name "
                        "FROM dim_material "
                        "WHERE material_pk in ( "
                        " SELECT material_pk FROM fact_material_measure "
                        " WHERE sequence_pk = :sequence_pk "
                        " AND date_pk = :date_pk"
                        ")"
                    ),
                    (
                        {
                            "sequence_pk": self.__seq_order,
                            "date_pk": DatePK(self.__date).value()
                        }
                    )
            ).fetchall():
                result.append(
                    PgBlendMaterial(
                        self.__date, self.__seq_order, row[0], self.__dwh
                    )
                )
        return result

    def add(self, material: BlendMaterial) -> BlendMaterial:
        if not self.has(material.name()):
            material_pk = self.__register_dim_mat(material.name())
            pit_pk = self.__register_dim_pit(material.pit())
            date_pk = DatePK(self.__date).value()
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.AU_GRADE, value=material.au_grade()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.SOL_CU, value=material.soluble_copper()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.ARSENIC, value=material.arsenic()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.MOISTURE, value=material.moisture()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.INDICATIVE_REC,
                value=material.indicative_rec()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.BUCKET, value=material.bucket()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.AVAILABLE_TONS,
                value=material.available_tons()
            )
            self.__register_measure(
                dim_mat_pk=material_pk, date_pk=date_pk, pit_pk=pit_pk,
                name=BlendMaterial.PROP, value=material.proportion()
            )
        return self.get(material.name())

    def __get_dim_mat_charac_uid(self, name: str) -> int:
        """
        Gets a dim material characteristic.
        :param name: Name
        :return: Key
        :raises ValueNotFoundError: If not found
        """
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT materialcharac_pk "
                    "FROM dim_material_charac "
                    "WHERE name = :name"
                ),
                (
                    {"name": name}
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError(
                    f"Material characteristic {name} not found"
                )
            return row["materialcharac_pk"]

    def __register_dim_mat(self, name: str) -> int:
        """
        Registers a dim material.
        :param name: Name
        :return: Key
        """
        with self.__dwh.connection() as conn:
            count, = conn.execute(
                text(
                    "SELECT count(*) "
                    "FROM dim_material  "
                    "WHERE name = :name"
                ),
                (
                    {"name": name}
                )
            ).fetchone()
            if count == 0:
                uid, = conn.execute(
                    text(
                        "INSERT INTO dim_material(name) "
                        "VALUES(:name) RETURNING material_pk "
                    ),
                    (
                        {"name": name}
                    )
                ).fetchone()
            else:
                uid, = conn.execute(
                    text(
                        "SELECT material_pk "
                        "FROM dim_material  "
                        "WHERE name = :name"
                    ),
                    (
                        {"name": name}
                    )
                ).fetchone()
            return uid

    def __register_dim_pit(self, name: str) -> int:
        """
        Registers a pit.
        :param name: Name
        :return: Key
        """
        with self.__dwh.connection() as conn:
            count, = conn.execute(
                text(
                    "SELECT count(*) "
                    "FROM dim_pit  "
                    "WHERE name = :name"
                ),
                (
                    {"name": name}
                )
            ).fetchone()
            if count == 0:
                uid, = conn.execute(
                    text(
                        "INSERT INTO dim_pit(name, abbreviation) "
                        "VALUES(:name, :abbreviation) RETURNING pit_pk "
                    ),
                    (
                        {"name": name, "abbreviation": name}
                    )
                ).fetchone()
            else:
                uid, = conn.execute(
                    text(
                        "SELECT pit_pk "
                        "FROM dim_pit  "
                        "WHERE name = :name"
                    ),
                    (
                        {"name": name}
                    )
                ).fetchone()
            return uid

    # pylint: disable=too-many-arguments
    def __register_measure(
        self, dim_mat_pk: int, date_pk: int, pit_pk: int,
        name: str, value: float
    ) -> None:
        """
        Registers measure.
        :param dim_mat_pk: Material UID
        :param date_pk: Date PK
        :param pit_pk: PIT PK
        :param name: Characteristic name
        :param value: Value
        """
        charac_pk = self.__get_dim_mat_charac_uid(name)
        with self.__dwh.connection() as conn:
            conn.execute(
                text(
                    "INSERT INTO fact_material_measure(date_pk, "
                    "sequence_pk, materialcharac_pk, pit_pk, "
                    "material_pk, value) "
                    "VALUES(:date_pk, :sequence_pk, :materialcharac_pk, "
                    ":pit_pk, :material_pk, :value) "
                ),
                (
                    {
                        "date_pk": date_pk,
                        "sequence_pk": self.__seq_order,
                        "materialcharac_pk": charac_pk,
                        "pit_pk": pit_pk,
                        "material_pk": dim_mat_pk,
                        "value": value
                    }
                )
            )
