# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_components.build import Factory
from .MemoryLock import MemoryLock
from .NullLock import NullLock


class DefaultLockFactory(Factory):
    """
    Creates :class:`ILock <pip_services4_logic.lock.ILock.ILock>` components by their descriptors.

    See :class:`Factory <pip_services4_logic.build.Factory.Factory>`,
    :class:`ILock <pip_services4_logic.lock.ILock.ILock>`,
    :class:`MemoryLock <pip_services4_logic.lock.MemoryLock.MemoryLock>`,
    :class:`NullLock <pip_services4_logic.lock.NullLock.NullLock>`
    """
    NullLockDescriptor = Descriptor("pip-services", "lock", "null", "*", "1.0")
    MemoryLockDescriptor = Descriptor("pip-services", "lock", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultLockFactory, self).__init__()
        self.register_as_type(DefaultLockFactory.NullLockDescriptor, NullLock)
        self.register_as_type(DefaultLockFactory.MemoryLockDescriptor, MemoryLock)
