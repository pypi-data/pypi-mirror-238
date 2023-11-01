# -*- coding: utf-8 -*-

import datetime
from typing import Any, Optional, List

from pip_services4_components.config import IReconfigurable, ConfigParams
from pip_services4_components.context.IContext import IContext

from .IStateStore import IStateStore
from .StateEntry import StateEntry
from .StateValue import StateValue


class MemoryStateStore(IStateStore, IReconfigurable):
    """
    State store that keeps states in the process memory.

    Remember: This implementation is not suitable for synchronization of distributed processes.

    ### Configuration parameters ###

        __options:__
        - timeout: default caching timeout in milliseconds (default: disabled)

    See: :class:`ICache <pip_services4_logic.cache.ICache.ICache>`

    Example:

    .. code-block:: python

        store = MemoryStateStore()

        value = store.load(Context.from_trace_id("123"), "key1")
        ...
        store.save("123", "key1", "ABC")
    """

    def __init__(self):
        """
        Creates a new instance of the state store.
        """
        self._states = {}
        self._timeout = 0

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._timeout = config.get_as_long_with_default("options.timeout", self._timeout)

    def __cleanup(self):
        if self._timeout == 0:
            return None

        cut_off_time = int(datetime.datetime.now().timestamp() * 1000) - self._timeout

        # Cleanup obsolete entries
        for prop in self._states:
            entry: StateEntry = self._states[prop]
            # Remove obsolete entry
            if entry.get_last_update_time() < cut_off_time:
                del self._states[prop]

    def load(self, context: Optional[IContext], key: str) -> Any:
        """
        Loads stored value from the store using its key.
        If value is missing in the store it returns None.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :return: the state value or `None` if value wasn't found.
        """
        if key is None:
            raise Exception("Key cannot be None")

        # Cleanup the stored states
        self.__cleanup()

        # Get entry from the store
        entry: StateEntry = self._states.get(key)

        # Store has nothing
        if entry is None:
            return None

        return entry.get_value()

    def load_bulk(self, context: Optional[IContext], keys: List[str]) -> List[StateValue]:
        """
        Loads an array of states from the store using their keys.

        :param context: (optional) transaction id to trace execution through call chain.
        :param keys: unique state keys.
        :return: an array with state values.
        """
        # Cleanup the stored states
        self.__cleanup()

        result = []

        for key in keys:
            value = self.load(context, key)
            result.append(StateValue(key, value))

        return result

    def save(self, context: Optional[IContext], key: str, value: Any) -> Any:
        """
        Saves state into the store

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :param value: a state value to store.
        :return: The value that was stored in the cache.
        """
        if key is None:
            raise Exception('Key cannot be None')

        # Cleanup the stored states
        self.__cleanup()

        # Get the entry
        entry: StateEntry = self._states.get(key)

        # Shortcut to remove entry from the cache
        if value is None:
            del self._states[key]
            return value

        # Update the entry
        if entry is not None:
            entry.set_value(value)
        # Or create a new entry
        else:
            entry = StateEntry(key, value)
            self._states[key] = entry

        return value

    def delete(self, context: Optional[IContext], key: str) -> Any:
        """
        Deletes a state from the store by its key.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :return: deleted item
        """
        if key is None:
            raise Exception('Key cannot be None')

        # Cleanup the stored states
        self.__cleanup()

        # Get the entry
        entry: StateEntry = self._states.get(key)

        # Remove entry from the cache
        if entry is not None:
            del self._states[key]
            return entry.get_value()

        return None
