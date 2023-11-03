"""
This module implements a fake PI tags.
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

from edv_dwh_connector.pi.pi_tag import PITag, PITags
from edv_dwh_connector.pi.cached.cached_pi_tag import CachedPITag


class FakePITags(PITags):
    """
    Fake PI tags.
    .. since: 0.3
    """

    def __init__(self) -> None:
        """
        Ctor.
        """
        self.__tags = []  # type: ignore
        self.__uid = 0

    def items(self) -> list:
        return self.__tags

    def add(self, code: str, name: str, uom: str, web_id: str) -> PITag:
        self.__uid = self.__uid + 1
        tag = CachedPITag(self.__uid, code, name, uom, web_id)
        self.__tags.append(tag)
        return tag
