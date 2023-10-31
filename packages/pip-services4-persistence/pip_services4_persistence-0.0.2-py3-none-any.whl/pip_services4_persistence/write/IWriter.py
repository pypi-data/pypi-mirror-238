# -*- coding: utf-8 -*-
"""
    pip_services3_data.IWriter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data writers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, Optional, TypeVar

from pip_services4_components.context import IContext

T = TypeVar('T')  # Declare type variable


class IWriter:
    """
    Interface for data processing components that can create, update and delete data items.
    """

    def create(self, context: Optional[IContext], item: T) -> T:
        """
        Creates a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: an item to be created.

        :return: created item
        """
        raise NotImplementedError('Method from interface definition')

    def update(self, context: Optional[IContext], item: T) -> T:
        """
        Updates a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: an item to be updated.

        :return: updated item
        """
        raise NotImplementedError('Method from interface definition')

    def delete_by_id(self, context: Optional[IContext], id: Any) -> T:
        """
        Deleted a data item by it's unique id.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of the item to be deleted

        :return: deleted item.
        """
        raise NotImplementedError('Method from interface definition')
