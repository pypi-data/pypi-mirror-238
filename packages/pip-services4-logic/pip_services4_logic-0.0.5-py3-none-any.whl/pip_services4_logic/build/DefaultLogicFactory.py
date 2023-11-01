from pip_services4_components.refer import Descriptor

from pip_services4_components.build import Factory
from pip_services4_logic.cache import MemoryCache, NullCache
from pip_services4_logic.lock import NullLock, MemoryLock
from pip_services4_logic.state import MemoryStateStore, NullStateStore


class DefaultLogicFactory(Factory):
    """
    Creates business logic components by their descriptors.

    See:
    :class:`Factory <pip_services4_components.build.Factory.Factory>`
    :class:`ICache <pip_services4_logic.cache.ICache.ICache>`
    :class:`MemoryCache <pip_services4_logic.cache.MemoryCache.MemoryCache>`
    :class:`NullCache <pip_services4_logic.cache.NullCache.NullCache>`
    """
    NullCacheDescriptor = Descriptor("pip-services", "cache", "null", "*", "1.0")
    MemoryCacheDescriptor = Descriptor("pip-services", "cache", "memory", "*", "1.0")
    NullLockDescriptor = Descriptor("pip-services", "lock", "null", "*", "1.0")
    MemoryLockDescriptor = Descriptor("pip-services", "lock", "memory", "*", "1.0")
    NullStateStoreDescriptor = Descriptor("pip-services", "state-store", "null", "*", "1.0")
    MemoryStateStoreDescriptor = Descriptor("pip-services", "state-store", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultLogicFactory.MemoryCacheDescriptor, MemoryCache)
        self.register_as_type(DefaultLogicFactory.NullCacheDescriptor, NullCache)
        self.register_as_type(DefaultLogicFactory.NullLockDescriptor, NullLock)
        self.register_as_type(DefaultLogicFactory.MemoryLockDescriptor, MemoryLock)
        self.register_as_type(DefaultLogicFactory.MemoryStateStoreDescriptor, MemoryStateStore)
        self.register_as_type(DefaultLogicFactory.NullStateStoreDescriptor, NullStateStore)