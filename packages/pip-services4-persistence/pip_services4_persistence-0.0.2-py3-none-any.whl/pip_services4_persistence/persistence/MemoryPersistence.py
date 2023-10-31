# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import threading
from copy import deepcopy
from typing import List, Any, Optional, TypeVar

from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences
from pip_services4_components.run import IOpenable, ICleanable
from pip_services4_observability.log import CompositeLogger

from pip_services4_data.query.PagingParams import PagingParams
from pip_services4_data.query.DataPage import DataPage

from pip_services4_persistence.read import ILoader
from pip_services4_persistence.write.ISaver import ISaver

filtered = filter

T = TypeVar('T')  # Declare type variable


class MemoryPersistence(IConfigurable, IReferenceable, IOpenable, ICleanable):
    """
    Abstract persistence component that stores data in memory.

    This is the most basic persistence component that is only
    able to store data items of any type. Specific CRUD operations
    over the data items must be implemented in child classes by
    accessing :func:`self._items` property and calling
    :func:`save` method.

    The component supports loading and saving items from another
    data source. That allows to use it as a base class for file
    and other types of persistence components that cache all data
    in memory.

     ### Configuration parameters ###
        - options:
            - max_page_size:       Maximum number of items returned in a single page (default: 100)

    ### References ###
        - `*:logger:*:*:1.0`   (optional) ILogger components to pass log messages

    Example:

    .. code-block:: python
    
        class MyMemoryPersistence(MemoryPersistence):

            def get_by_name(self, context, name):
                item = self.find(name)
                ...
                return item

        persistence = MyMemoryPersistence()

        persistence.set(Context.from_trace_id("123"), MyData("ABC"))
        print str(persistence.get_by_name(Context.from_trace_id("123"), "ABC")))
    """

    def __init__(self, loader: ILoader = None, saver: ISaver = None):
        """
        Creates a new instance of the persistence.

        :param loader: (optional) a loader to load items from external datasource.

        :param saver: (optional) a saver to save items to external datasource.
        """
        self._lock: threading.Lock = threading.Lock()
        self._logger: CompositeLogger = CompositeLogger()
        self._items: List[Any] = []
        self._loader: ILoader = loader
        self._saver: ISaver = saver
        self._opened: bool = False
        self._max_page_size = 100

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._max_page_size = config.get_as_integer_with_default("options.max_page_size", self._max_page_size)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: Anyrue if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        self.load(context)
        self._opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        self.save(context)
        self._opened = False

    def load(self, context: Optional[IContext]):
        """
        TODO add description
        """
        if self._loader is None: return

        with self._lock:
            self._items = self._loader.load(context)

        self._logger.trace(context, "Loaded " + str(len(self._items)) + " items")

    def save(self, context: Optional[IContext]):
        """
        Saves items to external data source using configured saver component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._saver is None: return

        with self._lock:
            self._saver.save(context, self._items)

        self._logger.trace(context, "Saved " + str(len(self._items)) + " items")

    def clear(self, context: Optional[IContext]):
        """
        Clears component state.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        with self._lock:
            del self._items[:]

        self._logger.trace(context, "Cleared items")

        # Outside of lock to avoid reentry
        self.save(context)

    def __convert_to_obj(self, item):
        if isinstance(item, dict):
            item = type('object', (object,), item)

        return item

    def create(self, context: Optional[IContext], item: T) -> T:
        """
        Creates a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: an item to be created.

        :return: a created item
        """
        with self._lock:
            item = self.__convert_to_obj(item)
            self._items.append(item)

        self._logger.trace(context, "Created " + str(item))

        # Avoid reentry
        self.save(context)
        return item

    def get_page_by_filter(self, context: Optional[IContext], filter: Any, paging: PagingParams, sort: Any = None,
                           select: Any = None) -> DataPage:
        """
        Gets a page of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public :func:`get_page_by_filter` method from child class that
        receives :class:`FilterParams <pip_services3_commons.data.FilterParams.FilterParams>` and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param paging: (optional) paging parameters

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data page of result by filter.
        """
        with self._lock:
            items = deepcopy(self._items)

        # Filter and sort
        if filter is not None:
            items = list(filtered(filter, items))
        if sort is not None:
            items = list(filtered(sort, items))
            # items = sorted(items, sort)

        # Prepare paging parameters
        paging = paging if paging is not None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)

        # Get a page
        data = items
        if skip > 0:
            data = data[skip:]
        if take > 0:
            data = data[:take]

        # Convert values
        if not (select is None):
            data = map(select, data)

        self._logger.trace(context, "Retrieved " + str(len(data)) + " items")

        # Return a page
        return DataPage(data, len(items))

    def get_list_by_filter(self, context: Optional[IContext], filter: Any,
                           sort: Any = None, select: Any = None) -> List[T]:
        """
        Gets a list of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public :func:`get_list_by_filter` method from child class that
        receives :class:`FilterParams <pip_services3_commons.data.FilterParams.FilterParams>` and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data list of results by filter.
        """
        with self._lock:
            items = deepcopy(self._items)

        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))
        if not (sort is None):
            items = list(sorted(items, key=sort))

        # Convert values      
        if not (select is None):
            items = map(select, items)

        # Return a list
        return list(items)

    def get_count_by_filter(self, context: Optional[IContext], filter: Any) -> int:
        """
        Gets a number of items retrieved by a given filter.

        This method shall be called by a public get_count_by_filter method from child class that
        receives FilterParams and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter function to filter items
        :return:  a number of data items that satisfy the filter.
        """

        with self._lock:
            items = deepcopy(self._items)

        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))

        self._logger.trace(context, f"Retrieved {len(items)} items")

        # Return a list
        return len(items)

    def get_one_random(self, context: Optional[IContext], filter: Any) -> T:
        """
        Gets a random item from items that match to a given filter.

        This method shall be called by a public :func:`get_one_random` method from child class
        that receives :class:`FilterParams <pip_services3_commons.data.FilterParams.FilterParams>` and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter function to filter items.

        :return: a random item.
        """
        with self._lock:
            if len(self._items) == 0:
                return None

            items = self._items

            # Apply filter
            if callable(filter):
                items = list(filtered(filter, items))

            index = random.randint(0, len(self._items))
            item = None if len(items) <= 0 else items[index]

        if not (item is None):
            self._logger.trace(context, "Retrieved a random item")
        else:
            self._logger.trace(context, "Nothing to return as random item")

        return item

    def delete_by_filter(self, context: Optional[IContext], filter: Any):
        """
        Deletes data items that match to a given filter.

        This method shall be called by a public :func:`delete_by_filter` method from child class that
        receives :class:`FilterParams <pip_services3_commons.data.FilterParams.FilterParams>` and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items.
        """

        def negative_filter(item):
            return not filter(item)

        old_length = len(deepcopy(self._items))

        with self._lock:
            self._items = list(filtered(negative_filter, self._items))

        deleted = old_length - len(deepcopy(self._items))
        self._logger.trace(context, "Deleted " + str(deleted) + " items")

        if deleted > 0:
            self.save(context)
