"""
This module defines Blend proposals.
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

# pylint: disable=duplicate-code
from datetime import date
from abc import ABC, abstractmethod
from edv_dwh_connector.blend_proposal.blend_sequence import BlendSequences
from edv_dwh_connector.exceptions import ValueNotFoundError


class BlendProposal(ABC):
    """
    Blend proposal.
    .. since: 0.1
    """

    @abstractmethod
    def date(self) -> date:
        """
        Gets date.
        :return: Date
        """

    @abstractmethod
    def sequences(self) -> BlendSequences:
        """
        Gets all sequences.
        :return: List of sequences
        """


class BlendProposals(ABC):
    """
    List of blend proposals.
    .. since: 0.1
    """

    @abstractmethod
    def last(self) -> BlendProposal:
        """
        Gets last.
        :return: Last blend
        """

    def has_at(self, dte: date) -> bool:
        """
        Has date.
        :param dte: Date
        :return: Has or not
        """
        contains = False
        for blend in self.items():
            if blend.date() == dte:
                contains = True
                break
        return contains

    def get_at(self, dte: date) -> BlendProposal:
        """
        Gets at date.
        :param dte: Date
        :return: Blend proposal
        :raises ValueNotFoundError: If not found
        """
        for blend in self.items():
            if blend.date() == dte:
                return blend
        raise ValueNotFoundError(
            f"Blend proposal not found at date {date}"
        )

    @abstractmethod
    def items(self, start: date = None, end: date = None) -> list:
        """
        Gets all items on period.
        :param start: Start date
        :param end: End date
        :return: List of items
        """

    @abstractmethod
    def add(self, blend: BlendProposal) -> BlendProposal:
        """
        Adds a blend proposal.
        :param blend: Blend proposal
        :return: Blend proposal
        """


class LocalBlendProposals(BlendProposals):
    """
    Blend proposals stored locally.
    .. since: 0.5
    """

    def __init__(self):
        """
        Ctor.
        """
        self.__blends = []

    def last(self) -> BlendProposal:
        return self.__blends[len(self.__blends) - 1]

    def items(self, start: date = None, end: date = None) -> list:
        if start is None or end is None:
            blends = self.__blends
        else:
            blends = []
            for blend in self.__blends:
                if start <= blend.date() <= end:
                    blends.append(blend)
        return blends

    def add(self, blend: BlendProposal) -> BlendProposal:
        self.__blends.append(blend)
        return blend
