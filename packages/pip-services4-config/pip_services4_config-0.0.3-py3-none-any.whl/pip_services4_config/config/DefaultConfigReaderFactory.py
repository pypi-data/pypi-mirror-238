# -*- coding: utf-8 -*-
"""
    pip_services4_config.connect.DefaultConfigReaderFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default discovery factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .JsonConfigReader import JsonConfigReader
from .MemoryConfigReader import MemoryConfigReader
from .YamlConfigReader import YamlConfigReader


class DefaultConfigReaderFactory(Factory):
    """
    Creates :class:`IConfigReader <pip_services4_config.config.IConfigReader.IConfigReader>` components by their descriptors.

    See :class:`Factory <pip_services4_components.build.Factory.Factory>`,
    :class:`MemoryConfigReader <pip_services4_config.config.MemoryConfigReader.MemoryConfigReader>`,
    :class:`JsonConfigReader <pip_services4_config.config.JsonConfigReader.JsonConfigReader>`,
    :class:`YamlConfigReader <pip_services4_config.config.YamlConfigReader.YamlConfigReader>`
    """

    MemoryConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "memory", "*", "1.0")
    JsonConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "json", "*", "1.0")
    YamlConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "yaml", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultConfigReaderFactory.MemoryConfigReaderDescriptor, MemoryConfigReader)
        self.register_as_type(DefaultConfigReaderFactory.JsonConfigReaderDescriptor, JsonConfigReader)
        self.register_as_type(DefaultConfigReaderFactory.YamlConfigReaderDescriptor, YamlConfigReader)
