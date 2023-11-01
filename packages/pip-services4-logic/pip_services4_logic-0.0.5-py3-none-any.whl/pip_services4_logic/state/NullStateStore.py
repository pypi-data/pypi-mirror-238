# -*- coding: utf-8 -*-

from typing import Optional, Any, List

from pip_services4_components.context.IContext import IContext

from .StateValue import StateValue
from .IStateStore import IStateStore


class NullStateStore(IStateStore):
    """
    Dummy state store implementation that doesn't do anything.

    It can be used in testing or in situations when state management is not required
    but shall be disabled.

    See: :class:`ICache <pip_services4_logic.cache.ICache.ICache>`
    """

    def load(self, context: Optional[IContext], key: str) -> Any:
        """
        Loads state from the store using its key.
        If value is missing in the stored it returns None.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :return: the state value or `None` if value wasn't found.
        """
        return None

    def load_bulk(self, context: Optional[IContext], keys: List[str]) -> List[StateValue]:
        """
        Loads an array of states from the store using their keys.

        :param context: (optional) transaction id to trace execution through call chain.
        :param keys: unique state keys.
        :return: an array with state values and their corresponding keys.
        """
        return []

    def save(self, context: Optional[IContext], key: str, value: Any) -> Any:
        """
        Saves state into the store.

        :param context: (optional) transaction id to trace execution throug
        :param key: a unique state key.
        :param value: a state value.
        :return: The state that was stored in the store.
        """
        return value

    def delete(self, context: Optional[IContext], key: str) -> Any:
        """
        Deletes a state from the store by its key.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique value key.
        :return: deleted item
        """
        return None



