"""
This module defines Blend sequence.
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
from datetime import date
from typing import Final

from edv_dwh_connector.blend_proposal.blend_material import BlendMaterials
from edv_dwh_connector.exceptions import ValueNotFoundError


class BlendSequence(ABC):
    """
    Blend sequence.
    .. since: 0.1
    """

    AU_GRADE: Final[str] = "Average Au Grade"

    ARSENIC: Final[str] = "Arsenic"

    SOLUBLE_COPPER: Final[str] = "Soluble Copper"

    MOISTURE_ESTIMATED: Final[str] = "Moisture Estimated"

    OXIDE_TRANSITION: Final[str] = "Percentage of Oxide/Transition"

    FRESH: Final[str] = "Percentage of Fresh"

    RECOVERY_BLEND: Final[str] = "Estimated Recovery Blend"

    @abstractmethod
    def date(self) -> date:
        """
        Gets date.
        :return: Date
        """

    @abstractmethod
    def order(self) -> int:
        """
        Gets order.
        :return: Number
        """

    @abstractmethod
    def name(self) -> str:
        """
        Gets name.
        :return: Name
        """

    @abstractmethod
    def average_au_grade(self) -> float:
        """
        Gets average grade.
        :return: Average grade
        """

    @abstractmethod
    def soluble_copper(self) -> float:
        """
        Gets soluble copper.
        :return: Soluble copper
        """

    @abstractmethod
    def arsenic(self) -> float:
        """
        Gets As.
        :return: As
        """

    @abstractmethod
    def moisture_estimated(self) -> float:
        """
        Gets moisture estimated.
        :return: Moisture in percent
        """

    @abstractmethod
    def oxide_transition(self) -> float:
        """
        Gets Oxide or Transition.
        :return: Oxide or Transition in percent
        """

    @abstractmethod
    def fresh(self) -> float:
        """
        Gets fresh.
        :return: Fresh in percent
        """

    @abstractmethod
    def recovery_blend_estimated(self) -> float:
        """
        Gets recovery blend estimated.
        :return: Recovery blend estimated in percent
        """

    @abstractmethod
    def materials(self) -> BlendMaterials:
        """
        Get list of materials.
        :return: List of materials
        """


class BlendSequences:
    """
    Blend sequences.
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

    def get(self, name: str) -> BlendSequence:
        """
        Gets by name.
        :param name: Name
        :return: Blend sequence
        :raises ValueNotFoundError: If not found
        """
        for item in self.items():
            if item.name().lower() == name.lower():
                return item
        raise ValueNotFoundError(
            f"Blend sequence with name {name} not found"
        )

    @abstractmethod
    def items(self) -> list:
        """
        Gets all items.
        :return: List of items
        """

    @abstractmethod
    def add(self, sequence: BlendSequence) -> BlendSequence:
        """
        Adds a blend sequence.
        :param sequence: Blend sequence
        :return: Blend sequence
        """
