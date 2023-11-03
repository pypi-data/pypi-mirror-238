"""
This module implements PI tag API saving in a CSV file.
.. since: 0.6
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

# pylint: disable=consider-using-with
import csv

from edv_dwh_connector.pi.writer import Writer


class CSVWriter(Writer):
    """
    CSV writer.
    .. since: 0.6
    """
    def __init__(self, filename: str):
        """
        Ctor.
        :param filename: File name
        """
        self.__fp = open(filename, 'w', encoding='utf8', newline='')
        self.__writer = csv.writer(self.__fp, delimiter=',')

    def close(self):
        self.__fp.close()

    def write(self, row: list):
        self.__writer.writerow(row)
