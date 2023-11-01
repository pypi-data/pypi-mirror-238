# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_components.build import Factory
from .MemoryStateStore import MemoryStateStore
from .NullStateStore import NullStateStore


class DefaultStateStoreFactory(Factory):
    """
    Creates :class:`IStateStore <pip_services4_logic.state.IStateStore.IStateStore>` components by their descriptors.

    See: :class:`Factory <pip_services4_logic.build.Factory.Factory>`,
    :class:`IStateStore <pip_services4_logic.state.IStateStore.IStateStore>`,
    :class:`MemoryStateStore <pip_services4_logic.state.MemoryStateStore.MemoryStateStore>`,
    :class:`NullStateStore <pip_services4_logic.state.NullStateStore.NullStateStore>`
    """
    descriptor = Descriptor("pip-services", "factory", "state-store", "default", "1.0")
    NullStateStoreDescriptor = Descriptor("pip-services", "state-store", "null", "*", "1.0")
    MemoryStateStoreDescriptor = Descriptor("pip-services", "state-store", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()

        self.register_as_type(DefaultStateStoreFactory.MemoryStateStoreDescriptor, MemoryStateStore)
        self.register_as_type(DefaultStateStoreFactory.NullStateStoreDescriptor, NullStateStore)
