"""
This module implements a PostgreSQL data warehouse.
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

import threading
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.engine.base import Connection  # type: ignore
from edv_dwh_connector.dwh import Dwh


# pylint: disable=too-many-arguments,too-few-public-methods
class PgDwh(Dwh):
    """
    PostgreSQL data warehouse.
    .. since: 0.1
    """

    def __init__(self, engine: Engine) -> None:
        """
        Ctor.
        :param engine: Engine
        """
        self.__engine = engine
        self.__local = threading.local()

    @classmethod
    def from_connection(
        cls, name: str, host: str, user: str, password: str, port: int
    ) -> Dwh:
        """
        Data warehouse from connection credentials.
        :param name: Database name
        :param host: Hostname or IP address
        :param user: Username
        :param password: Password
        :param port: Port
        :return: Dwh
        """
        return PgDwh(
            create_engine(
                f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
            )
        )

    def connection(self) -> Connection:
        if getattr(self.__local, 'trx', None) is None:
            conn = self.__engine.connect()
        else:
            conn = NotCloseableConnection(
                self.__engine, self.__local.trx.conn.connection
            )
        return conn

    def begin(self):
        self.__local.trx = self.__engine.begin()
        return self.__local.trx

    def terminate(self) -> None:
        self.__local.trx.conn.close()
        self.__local.trx = None

    def engine(self) -> Engine:
        return self.__engine


# pylint: disable=abstract-method
class NotCloseableConnection(Connection):
    """
    Not closeable connection.
    .. since: 0.8
    """

    def __init__(self, engine, connection):
        """
        Ctor.
        :param engine: Engine
        :param connection: Connection
        """
        super().__init__(
            engine,
            connection
        )
        self._is_future = True

    def close(self):
        """
        Close.
        """

    def rollback(self):
        """
        Rollback.
        """

    def commit(self):
        """
        Commit.
        """
