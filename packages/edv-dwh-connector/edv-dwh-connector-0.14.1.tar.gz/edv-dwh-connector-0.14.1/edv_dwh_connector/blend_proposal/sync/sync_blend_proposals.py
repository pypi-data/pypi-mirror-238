"""
This module defines blend proposals synchronized with Database.
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

from edv_dwh_connector.blend_proposal.blend_proposal\
    import BlendProposals, BlendProposal
from edv_dwh_connector.sync_data import SyncData


class SyncBlendProposals(BlendProposals, SyncData):
    """
    Blend proposals synchronized with Database.
    .. since: 0.5
    """

    def __init__(self, src: BlendProposals, target: BlendProposals) -> None:
        """
        Ctor.
        :param src: Source
        :param target: Target
        """
        self.__src = src
        self.__target = target
        self.__synchronized = False

    def last(self) -> BlendProposal:
        self.synchronize()
        return self.__target.last()

    def items(self, start: date = None, end: date = None) -> list:
        self.synchronize()
        return self.__target.items(start, end)

    def synchronize(self) -> None:
        if not self.__synchronized:
            for blend in self.__src.items():
                self.__target.add(blend)
            self.__synchronized = True

    def get_at(self, dte: date) -> BlendProposal:
        return self.__target.get_at(dte)

    def has_at(self, dte: date) -> bool:
        return self.__target.has_at(dte)

    def add(self, blend: BlendProposal) -> BlendProposal:
        return self.__target.add(blend)
