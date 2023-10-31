# -*- coding: utf-8 -*-
"""
    pip_services3_data.ISetter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data setters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional, TypeVar

from pip_services4_components.context import IContext

T = TypeVar('T')  # Declare type variable


class ISetter:
    """
    Interface for data processing components that can set (create or update) data items.
    """

    def set(self, context: Optional[IContext], item: T) -> T:
        """
        Sets a data item. If the data item exists it updates it, otherwise it create a new data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: a item to be set.

        :return: updated item
        """
        raise NotImplementedError('Method from interface definition')
