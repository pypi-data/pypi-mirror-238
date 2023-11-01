# -*- coding: utf-8 -*-
from abc import ABC
from typing import Optional

from pip_services4_components.context.IContext import IContext

class ILock(ABC):
    """
    Interface for locks to synchronize work or parallel processes and to prevent collisions.

    The lock allows to manage multiple locks identified by unique keys.
    """

    def try_acquire_lock(self, context: Optional[IContext], key: str, ttl: int) -> bool:
        """
        Makes a single attempt to acquire a lock by its key.
        It returns immediately a positive or negative result.

        :param context:  (optional) transaction id to trace execution through call chain.
        :param key:             a unique lock key to acquire.
        :param ttl:             a lock timeout (time to live) in milliseconds.
        :return:                lock result
        """

    def acquire_lock(self, context: Optional[IContext], key: str, ttl: int, timeout: int):
        """
        Releases prevously acquired lock by its key.

        :param context:  (optional) transaction id to trace execution through call chain.
        :param key:             a unique lock key to acquire.
        :param ttl:             a lock timeout (time to live) in milliseconds.
        :param timeout:         lock timeout
        """

    def release_lock(self, context: Optional[IContext], key: str):
        """
        Releases prevously acquired lock by its key.
        
        :param context:  (optional) transaction id to trace execution through call chain.
        :param key:             a unique lock key to acquire.
        """
