# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pip_services4_components.context.IContext import IContext

from .StateValue import StateValue


class IStateStore(ABC):
    """
    Interface for state storages that are used to store and retrieve transaction states.
    """

    @abstractmethod
    def load(self, context: Optional[IContext], key: str) -> Any:
        """
        Loads state from the store using its key.
        If value is missing in the store it returns None.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :return: the state value or `None` if value wasn't found.
        """

    @abstractmethod
    def load_bulk(self, context: Optional[IContext], keys: List[str]) -> List[StateValue]:
        """
        Loads an array of states from the store using their keys.

        :param context: (optional) transaction id to trace execution through call chain.
        :param keys: unique state keys.
        :return: an array with state values and their corresponding keys.
        """
        raise NotImplementedError('Method from interface definition')

    @abstractmethod
    def save(self, context: Optional[IContext], key: str, value: Any) -> Any:
        """
        Saves state into the store.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique state key.
        :param value: a state value.
        :return: The state that was stored in the store.
        """
        raise NotImplementedError('Method from interface definition')

    @abstractmethod
    def delete(self, context: Optional[IContext], key: str) -> Any:
        """
        Deletes a state from the store by its key.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique value key.
        :return: deleted item
        """
