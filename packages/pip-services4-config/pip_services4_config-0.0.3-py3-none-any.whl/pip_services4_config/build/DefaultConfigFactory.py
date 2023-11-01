from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from pip_services4_config.auth import MemoryCredentialStore
from pip_services4_config.config import MemoryConfigReader, JsonConfigReader, YamlConfigReader
from pip_services4_config.connect import MemoryDiscovery


class DefaultConfigFactory(Factory):
    """
    Creates :class:`ICredentialStore <pip_services4_config.auth.ICredentialStore.ICredentialStore>` components by their descriptors.
    See:
    :class:`IFactory <pip_services4_components.build.IFactory.IFactory>`
    :class:`ICredentialStore <pip_services4_config.auth.ICredentialStore.ICredentialStore>`
    :class:`MemoryCredentialStore <pip_services4_config.auth.MemoryCredentialStore.MemoryCredentialStore>`
    """
    MemoryCredentialStoreDescriptor = Descriptor("pip-services", "credential-store", "memory", "*", "1.0")
    MemoryConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "memory", "*", "1.0")
    JsonConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "json", "*", "1.0")
    YamlConfigReaderDescriptor = Descriptor("pip-services", "config-reader", "yaml", "*", "1.0")
    MemoryDiscoveryDescriptor = Descriptor("pip-services", "discovery", "memory", "*", "1.0")

    def __init__(self):
        super().__init__()

        self.register_as_type(DefaultConfigFactory.MemoryCredentialStoreDescriptor, MemoryCredentialStore)
        self.register_as_type(DefaultConfigFactory.MemoryConfigReaderDescriptor, MemoryConfigReader)
        self.register_as_type(DefaultConfigFactory.JsonConfigReaderDescriptor, JsonConfigReader)
        self.register_as_type(DefaultConfigFactory.YamlConfigReaderDescriptor, YamlConfigReader)
        self.register_as_type(DefaultConfigFactory.MemoryDiscoveryDescriptor, MemoryDiscovery)
