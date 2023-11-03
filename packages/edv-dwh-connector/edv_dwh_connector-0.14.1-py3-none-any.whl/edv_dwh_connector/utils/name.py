"""
This module defines names.
.. since: 0.8
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
from abc import ABC, abstractmethod


class Name(ABC):
    """
    Name.
    .. since: 0.8
    """

    @abstractmethod
    def value(self) -> str:
        """
        Gets value.
        :return: Value
        """


class NameInLowercaseWithoutSpecialCharacterAndUnit(Name):
    """
    Name in lower case without special character and unit.
    .. since: 0.8
    """

    def __init__(self, name: str):
        """
        Ctor.
        :param name: Name to adapt
        """
        self.__name = name

    def value(self) -> str:
        result = self.__name
        pos = result.find('(')
        if pos > -1:
            result = result[0:pos]
        return result.replace(' ', '').replace('_', '').lower()
