# -*- coding: utf-8 -*-
"""
    pip_services3_data.ILoader
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data loaders.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import List, Optional, TypeVar

from pip_services4_components.context import IContext

T = TypeVar('T')  # Declare type variable


class ILoader(ABC):
    """
    Interface for data processing components that load data items.
    """

    def load(self, context: Optional[IContext]) -> List[T]:
        """
        Loads data items.

        :param context: (optional) transaction id to trace execution through call chain.

        :return: a list of data items
        """
        raise NotImplementedError('Method from interface definition')
