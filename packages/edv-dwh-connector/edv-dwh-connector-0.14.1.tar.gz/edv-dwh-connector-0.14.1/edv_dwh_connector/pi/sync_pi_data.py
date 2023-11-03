"""
This module defines Synchronized PI data.
.. since: 0.3
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

# pylint: disable=too-few-public-methods
import logging
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.pi.csv.csv_writer import CSVWriter
from edv_dwh_connector.sync_data import SyncData
from edv_dwh_connector.pi.pi_tag import PITags
from edv_dwh_connector.utils.periods import Periods
from edv_dwh_connector.pi_web_api_client import PiWebAPIClient
from edv_dwh_connector.pi.db.pg_pi_measure\
    import PgPIMeasures, OutputDwhTableLikePIMeasures
from edv_dwh_connector.pi.rest.rest_sync_pi_measures import RestSyncPIMeasures
from edv_dwh_connector.exceptions import NetworkError


class SyncPIDataRestToDwh(SyncData):
    """
    PI data that is synchronized from Rest API to DWH.
    .. since: 0.3
    """

    def __init__(
        self, tags: PITags, periods: Periods,
        client: PiWebAPIClient, dwh: Dwh
    ):
        """
        Ctor.
        :param tags: Tags
        :param periods: Periods where to synchronize
        :param client: Rest API client
        :param dwh: DWH
        """
        self.__tags = tags
        self.__periods = periods
        self.__client = client
        self.__dwh = dwh

    def synchronize(self) -> None:
        for tag in self.__tags.items():
            try:
                RestSyncPIMeasures(
                    self.__client, tag, self.__periods,
                    PgPIMeasures(tag, self.__dwh)
                ).synchronize()
            except NetworkError as error:
                logging.info(error)


class SyncPIDataRestToCSVDwhLike(SyncData):
    """
    PI data that is synchronized from Rest API to CSV in Dwh table format.
    .. since: 0.6
    """

    def __init__(
        self, tags: PITags, periods: Periods,
        client: PiWebAPIClient, file: str
    ):
        """
        Ctor.
        :param tags: Tags
        :param periods: Periods where to synchronize
        :param client: Rest API client
        :param file: File
        """
        self.__tags = tags
        self.__periods = periods
        self.__client = client
        self.__file = file

    def synchronize(self) -> None:
        writer = CSVWriter(self.__file)
        try:
            for tag in self.__tags.items():
                try:
                    RestSyncPIMeasures(
                        client=self.__client,
                        tag=tag,
                        periods=self.__periods,
                        target=OutputDwhTableLikePIMeasures(tag, writer)
                    ).synchronize()
                except NetworkError as error:
                    logging.info(error)
        finally:
            writer.close()
