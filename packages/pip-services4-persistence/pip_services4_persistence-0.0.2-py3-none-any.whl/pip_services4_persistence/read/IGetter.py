# -*- coding: utf-8 -*-
"""
    pip_services3_data.IGetter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data getters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, Optional, TypeVar

from pip_services4_components.context import IContext

from pip_services4_data.data.IIdentifiable import IIdentifiable

T = TypeVar('T')  # Declare type variable


class IGetter(IIdentifiable):
    """
    Interface for data processing components that can get data items.
    """

    def get_one_by_id(self, context: Optional[IContext], id: Any) -> T:
        """
        Gets a data items by its unique id.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of item to be retrieved.

        :return: an item by its id.
        """
        raise NotImplementedError('Method from interface definition')
