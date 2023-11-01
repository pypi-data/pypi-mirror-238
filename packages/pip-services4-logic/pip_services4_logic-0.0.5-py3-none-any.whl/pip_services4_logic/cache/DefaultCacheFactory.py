# -*- coding: utf-8 -*-
"""
    pip_services4_logic.cache.DefaultCacheFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default cache factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .MemoryCache import MemoryCache
from .NullCache import NullCache


class DefaultCacheFactory(Factory):
    """
    Creates :class:`ICache <pip_services4_logic.cache.ICache.ICache>` components by their descriptors.

    See :class:`Factory <pip_services4_logic.build.Factory.Factory>`,
    :class:`ICache <pip_services4_logic.cache.ICache.ICache>`,
    :class:`MemoryCache <pip_services4_logic.cache.MemoryCache.MemoryCache>`,
    :class:`NullCache <pip_services4_logic.cache.NullCache.NullCache>`
    """

    NullCacheDescriptor = Descriptor("pip-services", "cache", "null", "*", "1.0")
    MemoryCacheDescriptor = Descriptor("pip-services", "cache", "memory", "*", "1.0")
    descriptor = Descriptor("pip-services", "factory", "cache", "default", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultCacheFactory.NullCacheDescriptor, NullCache)
        self.register_as_type(DefaultCacheFactory.MemoryCacheDescriptor, MemoryCache)
