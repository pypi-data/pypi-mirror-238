"""
This module implements PI tag API coming from PostgreSQL.
.. since: 0.2
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

from sqlalchemy import text  # type: ignore
from edv_dwh_connector.pi.pi_tag import PITag, PITags
from edv_dwh_connector.pi.cached.cached_pi_tag import CachedPITag
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import ValueAlreadyExistsError,\
    ValueNotFoundError


class PgPITag(PITag):
    """
    PI Tag from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, uid: int, dwh: Dwh) -> None:
        """
        Ctor.
        :param uid: Unique identifier
        :param dwh: Data warehouse
        :raises ValueNotFoundError: If not found
        """
        self.__uid = uid
        with dwh.connection() as conn:
            self.__row = conn.execute(
                text(
                    "SELECT code, name, uom, web_id "
                    "FROM dim_pi_tag "
                    "WHERE tag_pk = :uid"
                ),
                ({"uid": self.__uid})
            ).fetchone()
            if self.__row is None:
                raise ValueNotFoundError("PI tag not found")

    def uid(self) -> int:
        return self.__uid

    def code(self) -> str:
        return self.__row["code"]

    def name(self) -> str:
        return self.__row["name"]

    def uom(self) -> str:
        return self.__row["uom"]

    def web_id(self) -> str:
        return self.__row["web_id"]


class PgPITags(PITags):
    """
    PI tags from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, dwh: Dwh):
        """
        Ctor.
        :param dwh: Data warehouse
        """
        self.__dwh = dwh

    def items(self) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT tag_pk FROM dim_pi_tag"
                )
            ).fetchall():
                result.append(
                    PgPITag(row[0], self.__dwh)
                )
        return result

    def add(self, code: str, name: str, uom: str, web_id: str) -> PITag:
        with self.__dwh.connection() as conn:
            count, = conn.execute(
                text(
                    "SELECT count(*) FROM dim_pi_tag "
                    f"WHERE code = '{code}'"
                )
            ).fetchone()
            if count == 0:
                uid, = conn.execute(
                    text(
                        "INSERT INTO dim_pi_tag(code, name, uom, web_id) "
                        "VALUES(:code, :name, :unit, :web_id) RETURNING tag_pk "  # noqa: E501
                    ),
                    ({"code": code, "name": name, "unit": uom, "web_id": web_id})  # noqa: E501
                ).fetchone()
                return PgPITag(uid, self.__dwh)
            raise ValueAlreadyExistsError(
                f"Tag with code {code} already exists"
            )


class PgCachedPITags(PITags):
    """
    Cached PI tags from PostgreSQL.
    .. since: 0.4
    """

    def __init__(self, dwh: Dwh):
        """
        Ctor.
        :param dwh: Data warehouse
        """
        self.__dwh = dwh

    def items(self) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT tag_pk, code, name, uom, web_id FROM dim_pi_tag"
                )
            ).fetchall():
                result.append(
                    CachedPITag(row[0], row[1], row[2], row[3], row[4])
                )
        return result

    def add(self, code: str, name: str, uom: str, web_id: str) -> PITag:
        raise NotImplementedError("We can't add new tag to a cached list")
