"""
This module defines PI tags that are synchronized with Rest API.
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

# pylint: disable=duplicate-code
import logging

from edv_dwh_connector.pi.pi_tag import PITags, PITag
from edv_dwh_connector.pi_web_api_client import PiWebAPIClient
from edv_dwh_connector.exceptions import NetworkError, ValueNotFoundError
from edv_dwh_connector.sync_data import SyncData


class RestSyncPITags(PITags, SyncData):
    """
    PI Tags synchronized with Rest API.
    .. since: 0.2
    """

    def __init__(
        self, server_id: str, client: PiWebAPIClient,
        codes: list, target: PITags
    ):
        """
        Ctor.
        :param server_id: PI server ID
        :param client: API client
        :param codes: List of tag codes
        :param target: Source to synchronized
        """
        self.__server_id = server_id
        self.__client = client
        self.__codes = codes
        self.__target = target
        self.__synchronized = False

    def has(self, code: str) -> bool:
        self.synchronize()
        contains = False
        if self.__target.has(code):
            for cde in self.__codes:
                if code.lower() == cde.lower():
                    contains = True
                    break
        return contains

    def get(self, code: str) -> PITag:
        self.synchronize()
        if self.has(code):
            return self.__target.get(code)
        raise ValueNotFoundError(f"Tag {code} not found")

    def items(self) -> list:
        self.synchronize()
        tags = []
        for item in self.__target.items():
            if self.has(item.code()):
                tags.append(item)
        return tags

    def add(self, code: str, name: str, uom: str, web_id: str) -> PITag:
        self.synchronize()
        return self.__target.add(code, name, uom, web_id)

    def synchronize(self) -> None:
        """
        Synchronizes tags with PI Server only once.
        :raises NetworkError: If network breaks
        :raises ValueError: If list of codes is empty
        """
        if not self.__synchronized:
            if len(self.__codes) == 0:
                raise ValueError('List of tags to synchronize is empty')
            endpoint = f"dataservers/{self.__server_id}/points"
            logging.info(
                "Fetching all tags from PI server with url %s",
                endpoint
            )
            response = self.__client.get(
                endpoint=endpoint
            )
            if response.status_code != 200:
                raise NetworkError(
                    f'Error {response.status_code} on PI server '
                    'when trying to fetch all tags'
                )
            jtags = response.json()
            for code in self.__codes:
                logging.info('Synchronizing tag %s', code)
                if not self.__target.has(code):
                    found = False
                    for jtag in jtags['Items']:
                        if jtag['Name'].lower() == code.lower():
                            found = True
                            logging.info('Saving tag %s', code)
                            name = jtag["Descriptor"].replace(
                                code.split('_')[0], ''
                            )
                            self.__target.add(
                                code, name, jtag["EngineeringUnits"],
                                jtag["WebId"]
                            )
                    if not found:
                        logging.info(
                            'Tag %s has not been found on PI server', code
                        )
            self.__synchronized = True
