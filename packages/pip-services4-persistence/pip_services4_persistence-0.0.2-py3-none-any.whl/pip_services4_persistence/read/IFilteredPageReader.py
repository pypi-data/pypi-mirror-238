# -*- coding: utf-8 -*-
"""
    pip_services3_data.IFilteredPageReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for filtered paging data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import SortParams, FilterParams
from pip_services4_data.query.PagingParams import PagingParams
from pip_services4_data.query.DataPage import DataPage


class IFilteredPageReader(ABC):
    """
    Interface for data processing components that can retrieve a page of data items by a filter.
    """

    def get_page_by_filter(self, context: Optional[IContext], filter: Optional[FilterParams],
                           paging: Optional[PagingParams],
                           sort: Optional[SortParams] = None) -> DataPage:
        """
        Gets a page of data items using filter parameters.

        :param context: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) filter parameters

        :param paging: (optional) paging parameters

        :param sort: (optional) sort parameters

        :return: list of items
        """
        raise NotImplementedError('Method from interface definition')
