# -*- coding: utf-8 -*-
"""
    pip_services4_config.auth.DefaultCredentialStoreFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default credential store factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.refer import Descriptor
from pip_services4_components.build import Factory

from .MemoryCredentialStore import MemoryCredentialStore


class DefaultCredentialStoreFactory(Factory):
    """
    Creates :class:`ICredentialStore <pip_services4_config.auth.ICredentialStore.ICredentialStore>`
     components by their descriptors.

    See :class:`IFactory <pip_services4_components.build.IFactory.IFactory>`,
    :class:`ICredentialStore <pip_services4_config.auth.ICredentialStore.ICredentialStore>`,
    :class:`MemoryCredentialStore <pip_services4_config.auth.MemoryCredentialStore.MemoryCredentialStore>`,
    """
    MemoryCredentialStoreDescriptor = Descriptor("pip-services", "credential-store", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(self.MemoryCredentialStoreDescriptor, MemoryCredentialStore)
