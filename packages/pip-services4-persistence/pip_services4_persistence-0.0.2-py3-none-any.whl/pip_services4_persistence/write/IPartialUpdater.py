# -*- coding: utf-8 -*-
"""
    pip_services3_data.IPartialUpdater
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for partial data updaters.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional, Any, TypeVar

from pip_services4_commons.data import AnyValueMap
from pip_services4_components.context import IContext

T = TypeVar('T')  # Declare type variable


class IPartialUpdater(ABC):
    """
    Interface for data processing components to update data items partially.
    """

    def update_partially(self, context: Optional[IContext], id: Any, data: AnyValueMap) -> T:
        """
        Updates only few selected fields in a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be updated.

        :param data: a map with fields to be updated.

        :return: updated item
        """
        raise NotImplementedError('Method from interface definition')
