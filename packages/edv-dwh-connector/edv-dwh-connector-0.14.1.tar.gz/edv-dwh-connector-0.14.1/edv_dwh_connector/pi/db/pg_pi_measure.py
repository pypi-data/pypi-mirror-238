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

# pylint: disable=duplicate-code, no-name-in-module
import os.path
from abc import abstractmethod
from datetime import datetime
import tempfile
import logging

import pandas as pd  # type: ignore
from dateutil import tz  # type: ignore
from psycopg2.errors import UniqueViolation  # type: ignore
from sqlalchemy import text  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore

from edv_dwh_connector.dwh import DatePK, TimePK, DatetimeFromPK
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import ValueNotFoundError, \
    ValueAlreadyExistsError
from edv_dwh_connector.pi.cached.cached_pi_measure import CachedPIMeasure
from edv_dwh_connector.pi.db.pg_pi_tag import PgPITag
from edv_dwh_connector.pi.pi_measure import PIMeasure, PIMeasures, PIMeasuresDf
from edv_dwh_connector.pi.pi_tag import PITag
# pylint: disable=line-too-long
from edv_dwh_connector.pi.writer import Writer


class PgPIMeasure(PIMeasure):
    """
    PI measure from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, date: datetime, dwh: Dwh) -> None:
        """
        Ctor.
        :param tag: PI tag
        :param date: Datetime
        :param dwh: Data warehouse
        :raises ValueNotFoundError: If not found
        """
        self.__tag = tag
        self.__date = datetime.strptime(
            date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "%Y-%m-%d %H:%M:%S.%f"
        ).astimezone(tz.UTC)
        with dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT value "
                    "FROM fact_pi_measure "
                    "WHERE tag_pk = :tag_pk"
                    " and date_pk = :date_pk and time_pk = :time_pk"
                    " and millisecond = :millis"
                ),
                (
                    {
                        "tag_pk": self.__tag.uid(),
                        "date_pk": DatePK(self.__date.date()).value(),
                        "time_pk": TimePK(self.__date.time()).value(),
                        "millis": int(self.__date.microsecond / 1000)
                    }
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("PI measure not found")
            self.__value = row["value"]

    def tag(self) -> PITag:
        return self.__tag

    def date(self) -> datetime:
        return self.__date

    def value(self) -> float:
        return float(self.__value)


class PgPIMeasures(PIMeasures):
    """
    PI measures from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag
        :param dwh: Data warehouse
        """
        self.__tag = tag
        self.__dwh = dwh

    def has_at(self, date: datetime) -> bool:
        has = True
        try:
            PgPIMeasure(self.__tag, date, self.__dwh)
        except ValueNotFoundError:
            has = False
        return has

    def last(self) -> PIMeasure:
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond FROM fact_pi_measure "  # noqa: E501
                    "ORDER BY date_pk DESC, time_pk DESC, millisecond DESC "
                    "LIMIT 1"
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("Last PI measure not found")
            return PgPIMeasure(
                self.__tag,
                DatetimeFromPK(row[0], row[1], row[2]).value(),
                self.__dwh
            )

    def items(self, start: datetime, end: datetime) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure "
                    "WHERE CAST(date_pk || '' || time_pk as bigint) BETWEEN :start AND :end and tag_pk = :tag_pk "  # noqa: E501
                ),
                (
                    {
                        "start": start.strftime('%Y%m%d%H%M%S'),
                        "end": end.strftime('%Y%m%d%H%M%S'),
                        "tag_pk": self.__tag.uid()
                    }
                )
            ).fetchall():
                result.append(
                    PgPIMeasure(
                        self.__tag,
                        DatetimeFromPK(row[0], row[1], row[2]).value(),
                        self.__dwh
                    )
                )
            for row in conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure_hist "
                    "WHERE CAST(date_pk || '' || time_pk as bigint) BETWEEN :start AND :end and tag_pk = :tag_pk "  # noqa: E501
                ),
                (
                    {
                        "start": start.strftime('%Y%m%d%H%M%S'),
                        "end": end.strftime('%Y%m%d%H%M%S'),
                        "tag_pk": self.__tag.uid()
                    }
                )
            ).fetchall():
                result.append(
                    PgPIMeasure(
                        self.__tag,
                        DatetimeFromPK(row[0], row[1], row[2]).value(),
                        self.__dwh
                    )
                )
        return result

    def add(self, date: datetime, value: float) -> PIMeasure:
        try:
            with self.__dwh.connection() as conn:
                conn.execute(
                    text(
                        "INSERT INTO fact_pi_measure "
                        "(tag_pk, date_pk, time_pk, value, millisecond) "
                        "VALUES"
                        "(:tag_pk, :date_pk, :time_pk, :value, :millis) "
                    ),
                    (
                        {
                            "tag_pk": self.__tag.uid(),
                            "date_pk": DatePK(date.date()).value(),
                            "time_pk": TimePK(date.time()).value(),
                            "value": value,
                            "millis": int(
                                date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                                .split(".")[1]
                            )
                        }
                    )
                )
                return PgPIMeasure(
                    self.__tag, date, self.__dwh
                )
        except IntegrityError as exe:
            assert isinstance(exe.orig, UniqueViolation)
            raise ValueAlreadyExistsError(
                "A measure already exists at "
                f"{date} for tag {self.__tag.code()}"
            ) from exe


class PgCachedPIMeasures(PIMeasures):
    """
    Cached PI measures from PostgreSQL.
    .. since: 0.4
    """

    def __init__(self, tag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag or code of tag
        :param dwh: Data warehouse
        """
        if isinstance(tag, str):
            self.__tag = PgPITag(
                PkTag(tag, dwh).value(), dwh
            )
        else:
            self.__tag = tag
        self.__dwh = dwh

    def has_at(self, date: datetime) -> bool:
        raise NotImplementedError(
            "We are not able to check now existence "
            "of a measure in a cached list"
        )

    def last(self) -> PIMeasure:
        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure "  # noqa: E501
                    "ORDER BY date_pk DESC, time_pk DESC, millisecond DESC "
                    "LIMIT 1"
                )
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("Last PI measure not found")
            return CachedPIMeasure(
                self.__tag,
                DatetimeFromPK(row[0], row[1], row[2]).value(),
                row[3]
            )

    def items(self, start: datetime, end: datetime) -> list:
        result = []
        start_time = TimePK(start.time()).value()
        end_time = TimePK(end.time()).value()
        if start_time and end_time == 0:
            end_time = 235959
        with self.__dwh.connection() as conn:
            for row in conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure "
                    "WHERE tag_pk = :tag_pk AND date_pk > :start AND date_pk < :end "  # noqa: E501
                    "UNION ALL "
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure "
                    "WHERE tag_pk = :tag_pk AND ((date_pk = :start AND time_pk >= :start_time_pk) OR (date_pk = :end AND time_pk <= :end_time_pk))"  # noqa: E501
                ),
                (
                    {
                        "start": DatePK(start).value(),
                        "end": DatePK(end).value(),
                        "start_time_pk": start_time,
                        "end_time_pk": end_time,
                        "tag_pk": self.__tag.uid()
                    }
                )
            ).fetchall():
                result.append(
                    CachedPIMeasure(
                        self.__tag,
                        DatetimeFromPK(row[0], row[1], row[2]).value(),
                        row[3]
                    )
                )
            for row in conn.execute(
                text(
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure_hist "
                    "WHERE tag_pk = :tag_pk AND date_pk > :start AND date_pk < :end "  # noqa: E501
                    "UNION ALL "
                    "SELECT date_pk, time_pk, millisecond, value "  # noqa: E501
                    "FROM fact_pi_measure_hist "
                    "WHERE tag_pk = :tag_pk AND ((date_pk = :start AND time_pk >= :start_time_pk) OR (date_pk = :end AND time_pk <= :end_time_pk))"  # noqa: E501
                ),
                (
                    {
                        "start": DatePK(start).value(),
                        "end": DatePK(end).value(),
                        "start_time_pk": start_time,
                        "end_time_pk": end_time,
                        "tag_pk": self.__tag.uid()
                    }
                )
            ).fetchall():
                result.append(
                    CachedPIMeasure(
                        self.__tag,
                        DatetimeFromPK(row[0], row[1], row[2]).value(),
                        row[3]
                    )
                )
        return result

    def add(self, date: datetime, value: float) -> PIMeasure:
        raise NotImplementedError(
            "We can't add a new measure in a cached list"
        )


class OutputDwhTableLikePIMeasures(PIMeasures):
    """
    Output PI measures like Dwh table.
    .. since: 0.6
    """

    def __init__(self, tag: PITag, writer: Writer):
        """
        Ctor.
        :param tag: Tag
        :param writer: Writer
        """
        self.__tag = tag
        self.__writer = writer

    def has_at(self, date: datetime) -> bool:
        raise NotImplementedError(
            "Has at not supported for output PI measures"
        )

    def last(self) -> PIMeasure:
        raise NotImplementedError(
            "Last not supported for output PI measures"
        )

    def items(self, start: datetime, end: datetime) -> list:
        raise NotImplementedError(
            "Gets items not supported for output PI measures"
        )

    def add(self, date: datetime, value: float) -> PIMeasure:  # type: ignore
        self.__writer.write(
            [
                self.__tag.uid(),
                DatePK(date.date()).value(),
                TimePK(date.time()).value(),
                int(
                    date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    .split(".")[1]
                ),
                value
            ]
        )


# pylint: disable=too-few-public-methods
class PgPIMeasuresDf(PIMeasuresDf):
    """
    PostgreSQL PI measures working with data frame.
    .. since: 0.9
    """

    def __init__(self, tag, dwh: Dwh, path: str = None):
        """
        Ctor.
        :param tag: Tag or code of tag
        :param dwh: Data warehouse
        :param path: Folder path where to store CSV files
        """
        if isinstance(tag, str):
            self._tag = PgPITag(
                PkTag(tag, dwh).value(), dwh
            )
        else:
            self._tag = tag
        self._dwh = dwh
        self._path = path

    def frame(self, start: datetime, end: datetime) -> pd.DataFrame:
        if self._path is None:
            logging.info('Fetching data without saving them')
            with tempfile.TemporaryFile() as file:
                dtf = self.__fetch(file, start, end)
        else:
            csv_file_path = os.path.join(
                self._path, f'{self._tag.code()}.csv'
            )
            if os.path.exists(csv_file_path):
                logging.info(
                    'Found a CSV file: %s. Fetching data from the file',
                    csv_file_path
                )
                with open(csv_file_path, 'r', encoding='utf8') as file:
                    dtf = PIMeasuresDf.load(file, self._tag.code())
            else:
                tmpfile = os.path.join(
                    self._path, f'{self._tag.code()}_WIP.csv'
                )
                if os.path.exists(tmpfile):
                    os.remove(tmpfile)
                with open(tmpfile, 'a+', encoding='utf8') as file:
                    logging.info(
                        'Fetching data from database and '
                        'saving them in a CSV file'
                    )
                    dtf = self.__fetch(file, start, end)
                os.rename(tmpfile, csv_file_path)
        return dtf

    def __fetch(self, file, start: datetime, end: datetime) -> pd.DataFrame:
        """
        Fetches data.
        :param file: CSV file
        :param start: Start date
        :param end: End date
        :return: DataFrame
        """
        # pylint: disable=consider-using-f-string
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
            query=self._sql(start, end),
            head="HEADER"
        )
        conn = self._dwh.engine().raw_connection()
        cur = conn.cursor()
        cur.copy_expert(copy_sql, file)
        file.seek(0)
        return PIMeasuresDf.load(file, self._tag.code())

    @abstractmethod
    def _sql(self, start: datetime, end: datetime) -> str:
        """
        SQL query.
        :param start: Start date
        :param end: End date
        :return: Query
        """


# pylint: disable=too-few-public-methods
class PgRecordedPIMeasuresDf(PgPIMeasuresDf):
    """
    PostgreSQL PI measures recorded working with data frame.
    .. since: 0.12
    """

    def _sql(self, start: datetime, end: datetime) -> str:
        return f"""
        {self.__sub_sql("fact_pi_measure", start, end)}\n
        UNION ALL\n
        {self.__sub_sql("fact_pi_measure_hist", start, end)}
        """

    def __sub_sql(self, table: str, start: datetime, end: datetime) -> str:
        """
        SQL query for a table.
        :param table: Table
        :param start: Start date
        :param end: End date
        :return: Query
        """
        start_num = DatePK(start).value()
        end_num = DatePK(end).value()
        start_time = TimePK(start.time()).value()
        end_time = TimePK(end.time()).value()
        if start_time and end_time == 0:
            end_time = 235959
        return f"""SELECT CAST(dd.date_value AS TEXT)||'T'||dt.time_value||'.'||LPAD(mea.millisecond::text, 3, '0') || 'Z' as DateTime, mea.value as {self._tag.code()}\n
        FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt\n
        WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk\n
        AND mea.tag_pk = {self._tag.uid()} AND mea.date_pk > {start_num} AND mea.date_pk < {end_num}\n
        UNION ALL\n
        SELECT CAST(dd.date_value AS TEXT)||'T'||dt.time_value||'.'||LPAD(mea.millisecond::text, 3, '0') || 'Z' as DateTime, mea.value as {self._tag.code()}\n
        FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt\n
        WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk\n
        AND mea.tag_pk = {self._tag.uid()} AND ((mea.date_pk = {start_num} AND mea.time_pk >= {start_time}) OR (mea.date_pk = {end_num} AND mea.time_pk <= {end_time}))"""  # noqa: E501


# pylint: disable=too-few-public-methods
class PgMinuteInterpolatedPIMeasuresDf(PgPIMeasuresDf):
    """
    PostgreSQL PI measures interpolated working with data frame.
    .. since: 0.12
    """

    def _sql(self, start: datetime, end: datetime) -> str:
        return f"""
        WITH paired_dates AS (
          SELECT LAG(date) OVER (ORDER BY date) AS lag_date
            , LAG(value) OVER (ORDER BY value) AS lag_mi
            , date AS obs_date
            , value AS obs_mi
          FROM(
            SELECT date, PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY value) value FROM (
                {self.__sub_sql("fact_pi_measure", start, end)}\n
                UNION ALL\n
                {self.__sub_sql("fact_pi_measure_hist", start, end)}
            ) tbl
            group by date
          ) tbl
        )
        SELECT measure_date DateTime,
            linear_interpolate(measure_date, lag_date, lag_mi::numeric, obs_date, obs_mi::numeric) as {self._tag.code()}
        FROM paired_dates
          , generate_series(lag_date, obs_date - INTERVAL '1 second', INTERVAL '1 minute') minutes (measure_date)
        """  # noqa: E501

    def __sub_sql(self, table: str, start: datetime, end: datetime) -> str:
        """
        SQL query for a table.
        :param table: Table
        :param start: Start date
        :param end: End date
        :return: Query
        """
        start_num = DatePK(start).value()
        end_num = DatePK(end).value()
        start_time = TimePK(start.time()).value()
        end_time = TimePK(end.time()).value()
        if start_time and end_time == 0:
            end_time = 235959
        return f"""SELECT TO_TIMESTAMP(CAST(dd.date_value AS TEXT)||' '||dt.hours_24||':'||dt.hour_minutes||':00', 'YYYY-MM-DD HH24:MI:SS') as date, mea.value\n
        FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt\n
        WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk\n
        AND mea.tag_pk = {self._tag.uid()} AND mea.date_pk > {start_num} AND mea.date_pk < {end_num}\n
        UNION ALL\n
        SELECT TO_TIMESTAMP(CAST(dd.date_value AS TEXT)||' '||dt.hours_24||':'||dt.hour_minutes||':00', 'YYYY-MM-DD HH24:MI:SS') as date, mea.value\n
        FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt\n
        WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk\n
        AND mea.tag_pk = {self._tag.uid()} AND ((mea.date_pk = {start_num} AND mea.time_pk >= {start_time}) OR (mea.date_pk = {end_num} AND mea.time_pk <= {end_time}))"""  # noqa: E501


class PkTag:
    """
    Primary key of tag.
    .. since: 0.9
    """

    def __init__(self, code: str, dwh: Dwh):
        """
        Ctor.
        :param code: Code
        :param dwh: Data warehouse
        """
        self.__code = code
        self.__dwh = dwh

    def value(self) -> int:
        """
        # noqa: DAR401
        # noqa: DAR003
        Gets value.
        :return: Value
        :raise ValueNotFoundError: If not found
        """

        with self.__dwh.connection() as conn:
            row = conn.execute(
                text(
                    "SELECT tag_pk "
                    "FROM dim_pi_tag "
                    "WHERE code = :code"
                ),
                ({"code": self.__code})
            ).fetchone()
            if row is None:
                raise ValueNotFoundError("PI tag not found")
            return row["tag_pk"]
