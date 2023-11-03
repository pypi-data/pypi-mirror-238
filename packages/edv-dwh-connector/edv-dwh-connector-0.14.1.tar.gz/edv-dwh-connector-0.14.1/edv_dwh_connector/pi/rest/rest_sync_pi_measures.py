"""
This module defines PI measures that are synchronized with Rest API.
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


import logging
from datetime import datetime

from dateutil import parser  # type: ignore
from edv_dwh_connector.pi.pi_tag import PITag
from edv_dwh_connector.pi.pi_measure import PIMeasure, PIMeasures
from edv_dwh_connector.pi_web_api_client import PiWebAPIClient
from edv_dwh_connector.exceptions import NetworkError, ValueAlreadyExistsError
from edv_dwh_connector.utils.periods import Periods
from edv_dwh_connector.sync_data import SyncData

# pylint: disable=too-many-arguments
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class RestSyncPIMeasures(PIMeasures, SyncData):
    """
    PI measures synchronized with Rest API only once.
    .. since: 0.3
    """

    def __init__(
        self, client: PiWebAPIClient, tag: PITag,
        periods: Periods, target: PIMeasures
    ):
        """
        Ctor.
        :param client: API client
        :param tag: Tag
        :param periods: Periods where to fetch
        :param target: Source to synchronized
        """
        self.__client = client
        self.__tag = tag
        self.__periods = periods
        self.__target = target
        self.__synchronized = False

    def has_at(self, date: datetime) -> bool:
        self.synchronize()
        return self.__target.has_at(date)

    def last(self) -> PIMeasure:
        self.synchronize()
        return self.__target.last()

    def items(self, start: datetime, end: datetime) -> list:
        self.synchronize()
        return self.__target.items(start, end)

    def add(self, date: datetime, value: float) -> PIMeasure:
        self.synchronize()
        return self.__target.add(date, value)

    def synchronize(self) -> None:
        """
        Synchronizes tag data with PI Server.
        :raises NetworkError: If network breaks
        :raises ValueError: If there is no period
        """
        if not self.__synchronized:
            logging.info(
                'Fetching data of tag %s from PI server',
                self.__tag.code()
            )
            if len(self.__periods.items()) == 0:
                raise ValueError("There is no period specified")
            # pylint: disable=unused-variable
            for idx, period in enumerate(self.__periods.items()):
                # pylint: disable=line-too-long
                endpoint = f"streamsets/recorded?webId={self.__tag.web_id()}&maxCount=150000" \
                           f"&startTime={RestSyncPIMeasures.__format_date(period.start())}" \
                           f"&endTime={RestSyncPIMeasures.__format_date(period.end())}"  # noqa: E501
                logging.info(
                    "Fetching data from url %s", endpoint
                )
                response = self.__client.get(
                    endpoint=endpoint
                )
                if response.status_code != 200:
                    raise NetworkError(
                        f'Error {response.status_code} on PI server '
                        f'when trying to fetch data of tag {self.__tag.code()}'
                    )
                data = RestSyncPIMeasures.__clean_data(
                    response.json()["Items"][0]["Items"]
                )
                length = len(data)
                if length == 0:
                    logging.info(
                        'Not found data for tag %s on period [%s, %s]',
                        self.__tag.code(),
                        period.start().strftime(DATETIME_FORMAT),
                        period.end().strftime(DATETIME_FORMAT)
                    )
                    continue
                logging.info(
                    'Found %s item(s) for tag %s on period [%s, %s]',
                    length,
                    self.__tag.code(),
                    period.start().strftime(DATETIME_FORMAT),
                    period.end().strftime(DATETIME_FORMAT)
                )
                for item in data:
                    try:
                        self.__target.add(
                            datetime.strptime(
                                parser.isoparse(item['Timestamp'])
                                    .strftime(DATETIME_FORMAT),
                                DATETIME_FORMAT
                            ),
                            item['Value']
                        )
                    except ValueAlreadyExistsError as error:
                        logging.info(error)
            self.__synchronized = True

    @staticmethod
    def __clean_data(items: dict) -> list:
        """
        Clean data.
        :param items: Raw items
        :return: Cleaned items
        """
        data = []
        if items is not None:
            for item in items:
                if item['Good'] is True:
                    data.append(item)
        return data

    @staticmethod
    def __format_date(date: datetime) -> str:
        """
        Format date.
        :param date: Datetime
        :return: Date in string
        """
        return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
