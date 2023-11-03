"""
This module defines PI tag API.
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

from abc import ABC, abstractmethod
from edv_dwh_connector.exceptions import ValueNotFoundError


class PITag(ABC):
    """
    PI tag.
    .. since: 0.2
    """

    @abstractmethod
    def uid(self) -> int:
        """
        Gets Unique Identifier.
        :return: UID
        """

    @abstractmethod
    def code(self) -> str:
        """
        Gets code.
        :return: Code
        """

    @abstractmethod
    def name(self) -> str:
        """
        Gets name.
        :return: Name
        """

    @abstractmethod
    def uom(self) -> str:
        """
        Gets Unit of measure.
        :return: Unit
        """

    @abstractmethod
    def web_id(self) -> str:
        """
        Gets web ID.
        :return: Web ID
        """


class PITags(ABC):
    """
    List of PI tags.
    .. since: 0.2
    """

    def has(self, code: str) -> bool:
        """
        Checks if it has code
        :param code: Code
        :return: Has or not
        """
        contains = True
        try:
            self.get(code)
        except ValueNotFoundError:
            contains = False
        return contains

    def get(self, code: str) -> PITag:
        """
        Gets tag by code
        :param code: Code
        :return: Tag
        :raises ValueNotFoundError: If not found
        """
        for tag in self.items():
            if tag.code().lower() == code.lower():
                return tag
        raise ValueNotFoundError("Tag not found")

    @abstractmethod
    def items(self) -> list:
        """
        Gets all tags
        :return: List of tags
        """

    @abstractmethod
    def add(self, code: str, name: str, uom: str, web_id: str) -> PITag:
        """
        Adds a tag.
        :param code: Code
        :param name: Name
        :param uom: Unit of measure
        :param web_id: Web ID
        :return: PITag registered
        :raises AlreadyExistsError: If a tag with same code already exists
        """
