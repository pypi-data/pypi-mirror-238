# -*- coding: utf-8 -*-
"""
    pip_services4_config.connect.DefaultDiscoveryFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default discovery factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .MemoryDiscovery import MemoryDiscovery


class DefaultDiscoveryFactory(Factory):
    """
    Creates :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>` components by their descriptors.

    See :class:`Factory <pip_services4_components.build.Factory.Factory>`,
    :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>`,
    :class:`MemoryDiscovery <pip_services4_config.connect.MemoryDiscovery.MemoryDiscovery>`,
    """

    MemoryDiscoveryDescriptor = Descriptor("pip-services", "discovery", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultDiscoveryFactory.MemoryDiscoveryDescriptor, MemoryDiscovery)
