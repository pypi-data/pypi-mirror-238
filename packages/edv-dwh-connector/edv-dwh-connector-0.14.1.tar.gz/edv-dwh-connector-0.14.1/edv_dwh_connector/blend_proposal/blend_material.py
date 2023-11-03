"""
This module defines a Blend material.
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

from abc import ABC, abstractmethod
from typing import Final

from edv_dwh_connector.exceptions import ValueNotFoundError


class BlendMaterial(ABC):
    """
    Blend Material.
    .. since: 0.1
    """

    AU_GRADE: Final[str] = "Au grade"

    SOL_CU: Final[str] = "Soluble copper"

    ARSENIC: Final[str] = "As"

    MOISTURE: Final[str] = "Moisture"

    INDICATIVE_REC: Final[str] = "Indicative Rec"

    BUCKET: Final[str] = "Bucket"

    AVAILABLE_TONS: Final[str] = "Available Tons"

    PROP: Final[str] = "Prop"

    @abstractmethod
    def machine(self) -> str:
        """
        Gets machine type.
        :return: Name
        """

    @abstractmethod
    def pit(self) -> str:
        """
        Gets a PIT.
        :return: PIT name
        """

    @abstractmethod
    def name(self) -> str:
        """
        Gets material name.
        :return: Material name
        """

    @abstractmethod
    def au_grade(self) -> float:
        """
        Gets Au grade.
        :return: Au grade
        """

    @abstractmethod
    def soluble_copper(self) -> float:
        """
        Gets Sol cu.
        :return: Sol cu
        """

    @abstractmethod
    def arsenic(self) -> float:
        """
        Gets As
        :return: As in ppm
        """

    @abstractmethod
    def moisture(self) -> float:
        """
        Gets Moisture.
        :return: Moisture
        """

    @abstractmethod
    def indicative_rec(self) -> float:
        """
        Get Indicative rec.
        :return: Indicative rec
        """

    @abstractmethod
    def bucket(self) -> float:
        """
        Gets bucket.
        :return: Bucket
        """

    @abstractmethod
    def available_tons(self) -> float:
        """
        Gets available tons.
        :return: Available tons
        """

    @abstractmethod
    def proportion(self) -> float:
        """
        Gets prop.
        :return: Prop
        """


class BlendMaterials:
    """
    Blend materials.
    .. since: 0.5
    """

    # pylint: disable=duplicate-code
    def has(self, name: str) -> bool:
        """
        Has name.
        :param name: Name
        :return: Has or not
        """
        contains = False
        for item in self.items():
            if item.name().lower() == name.lower():
                contains = True
                break
        return contains

    def get(self, name: str) -> BlendMaterial:
        """
        Gets by name.
        :param name: Name
        :return: Blend material
        :raises ValueNotFoundError: If not found
        """
        for item in self.items():
            if item.name().lower() == name.lower():
                return item
        raise ValueNotFoundError(
            f"Blend material {name} not found"
        )

    @abstractmethod
    def items(self) -> list:
        """
        Gets all items.
        :return: List of items
        """

    @abstractmethod
    def add(self, material: BlendMaterial) -> BlendMaterial:
        """
        Adds a blend material.
        :param material: Blend material
        :return Blend material
        """
