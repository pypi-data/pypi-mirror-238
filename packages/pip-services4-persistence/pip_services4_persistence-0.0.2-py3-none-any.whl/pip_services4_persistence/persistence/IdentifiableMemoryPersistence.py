# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.IdentifiableMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Identifiable memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional, Any, List, TypeVar

from pip_services4_commons.data import AnyValueMap
from pip_services4_components.context import IContext
from pip_services4_data.data import IIdentifiable
from pip_services4_data.keys import IdGenerator

from .MemoryPersistence import MemoryPersistence
from ..read import IGetter, ILoader
from ..write import ISaver
from ..write.ISetter import ISetter
from ..write.IWriter import IWriter

# This function will be overriden in the code
filtered = filter

T = TypeVar('T')  # Declare type variable


class IdentifiableMemoryPersistence(MemoryPersistence, IWriter, IGetter, ISetter, IIdentifiable):
    """
    Abstract persistence component that stores data in memory
    and implements a number of CRUD operations over data items
    with unique ids. The data items must implement IIdentifiable
    interface.

    In basic scenarios child classes shall only override
    :func:`get_page_by_filter`, :func:`get_list_by_filter` or :func:`delete_by_filter`
    operations with specific filter function. All other operations
    can be used out of the box.

    In complex scenarios child classes can implement additional
    operations by accessing cached items via this._items property
    and calling :func:`save` method on updates.

    ### Configuration parameters ###
        - options:
            - max_page_size:       Maximum number of items returned in a single page (default: 100)

    ### References ###
        - `*:logger:*:*:1.0`       (optional) ILogger components to pass log messages

    Example:

    .. code-block:: python

        class MyMemoryPersistence(IdentifiableMemoryPersistence):

            def get_page_by_filter(self, context, filter, paging):
                super().get_page_by_filter(context, filter, paging, None)

            persistence = MyMemoryPersistence("./data/data.json")

            item = persistence.create(Context.from_trace_id("123"), MyData("1", "ABC"))

            mydata = persistence.get_page_by_filter(Context.from_trace_id("123"), FilterParams.from_tuples("name", "ABC"), None, None)
            print str(mydata.get_data())

            persistence.delete_by_id("123", "1")
    """

    def __init__(self, loader: ILoader = None, saver: ISaver = None):
        """
        Creates a new instance of the persistence.

        :param loader: (optional) a loader to load items from external datasource.

        :param saver: (optional) a saver to save items to external datasource.
        """
        super(IdentifiableMemoryPersistence, self).__init__(loader, saver)

    def __convert_to_obj(self, item):
        if isinstance(item, dict):
            item = type('object', (object,), item)

        return item

    def get_list_by_ids(self, context: Optional[IContext], ids: List[Any]) -> List[T]:
        """
        Gets a list of data items retrieved by given unique ids.

        :param context: (optional) transaction id to trace execution through call chain.

        :param ids: ids of data items to be retrieved

        :return: a data list of results by ids.
        """

        def filter(item):
            item = self.__convert_to_obj(item)
            return item.id in ids

        return self.get_list_by_filter(context, filter)

    def _find_one(self, id: str):
        for item in self._items:
            if item.id == id:
                return item
        return None

    def get_one_by_id(self, context: Optional[IContext], id: Any) -> T:
        """
        Gets a data item by its unique id.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be retrieved.

        :return: data item by id.
        """
        with self._lock:
            item = self._find_one(id)

        if not (item is None):
            self._logger.trace(context, "Retrieved " + str(item) + " by " + str(id))
        else:
            self._logger.trace(context, "Cannot find item by " + str(id))
        return item

    def create(self, context: Optional[IContext], item: T) -> T:
        """
        Creates a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: an item to be created.

        :return: a created item
        """
        item = self.__convert_to_obj(item)

        if not hasattr(item, 'id') or item.id is None:
            item.id = IdGenerator.next_long()

        return super().create(context, item)

    def set(self, context: Optional[IContext], item: T) -> T:
        """
        Sets a data item. If the data item exists it updates it, otherwise it create a new data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param item: an item to be set.

        :return: an updated item
        """
        item = self.__convert_to_obj(item)

        if not hasattr(item, 'id') or item.id is None:
            item.id = IdGenerator.next_long()

        with self._lock:
            old_item = self._find_one(item.id)
            if old_item is None:
                self._items.append(item)
            else:
                index = self._items.index(old_item)
                if index < 0:
                    self._items.append(item)
                else:
                    self._items[index] = item

        self._logger.trace(context, "Set " + str(item))

        # Avoid reentry
        self.save(context)
        return item

    def update(self, context: Optional[IContext], new_item: T) -> T:
        """
        Updates a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param new_item: an item to be updated.

        :return: an updated item.
        """
        with self._lock:
            new_item = self.__convert_to_obj(new_item)

            old_item = self._find_one(new_item.id)
            if old_item is None:
                return None

            index = self._items.index(old_item)
            if index < 0: return None

            self._items[index] = new_item

        self._logger.trace(context, "Updated " + str(new_item))

        # Avoid reentry
        self.save(context)
        return new_item

    def update_partially(self, context: Optional[IContext], id: Any, data: AnyValueMap) -> T:
        """
        Updates only few selected fields in a data item.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be updated.

        :param data: a map with fields to be updated.

        :return: an updated item.
        """
        new_item = None

        with self._lock:
            old_item = self._find_one(id)
            if old_item is None:
                return None

            for k, v in data.items():
                setattr(old_item, k, v)

            new_item = old_item

        self._logger.trace(context, "Partially updated " + str(old_item))

        # Avoid reentry
        self.save(context)
        return new_item

    def delete_by_id(self, context: Optional[IContext], id: Any) -> T:
        """
        Deleted a data item by it's unique id.

        :param context: (optional) transaction id to trace execution through call chain.

        :param id: an id of the item to be deleted

        :return: a deleted item.
        """
        with self._lock:
            item = self._find_one(id)
            if item is None: return None

            index = self._items.index(item)
            if index < 0: return None

            del self._items[index]

        self._logger.trace(context, "Deleted " + str(item))

        self.save(context)
        return item

    def delete_by_ids(self, context: Optional[IContext], ids: List[Any]):
        """
        Deletes multiple data items by their unique ids.

        :param context: (optional) transaction id to trace execution through call chain.

        :param ids: ids of data items to be deleted.
        """

        def filter(item):
            item = self.__convert_to_obj(item)

            return item.id in ids

        self.delete_by_filter(context, filter)
