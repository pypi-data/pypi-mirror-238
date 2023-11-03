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

from edv_dwh_connector.pi.pi_tag import PITag


class CachedPITag(PITag):
    """
    Cached PI Tag.
    .. since: 0.4
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, uid: int, code: str, name: str, uom: str, web_id: str
    ) -> None:
        """
        Ctor.
        :param uid: Unique identifier
        :param code: Code
        :param name: Name
        :param uom: Unit of measure
        :param web_id: Web ID
        """
        self.__uid = uid
        self.__code = code
        self.__name = name
        self.__uom = uom
        self.__web_id = web_id

    def uid(self) -> int:
        return self.__uid

    def code(self) -> str:
        return self.__code

    def name(self) -> str:
        return self.__name

    def uom(self) -> str:
        return self.__uom

    def web_id(self) -> str:
        return self.__web_id
