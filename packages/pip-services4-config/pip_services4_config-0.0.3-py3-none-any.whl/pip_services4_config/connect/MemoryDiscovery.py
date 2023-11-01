# -*- coding: utf-8 -*-
"""
    pip_services4_config.connect.MemoryDiscovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory discovery implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import List, Optional

from pip_services4_components.config import IReconfigurable, ConfigParams
from pip_services4_components.context import IContext

from .ConnectionParams import ConnectionParams
from .IDiscovery import IDiscovery


class DiscoveryItem:
    """
    Used to store key-identifiable information about connections.
    """
    key: str = None
    connection: ConnectionParams = None


class MemoryDiscovery(IDiscovery, IReconfigurable):
    """
    Discovery service that keeps connections in memory.

    ### Configuration parameters ###
        - [connection key 1]:
        - ...                          connection parameters for key 1
        - [connection key 2]:
        - ...                          connection parameters for key N

    Example:

    .. code-block:: python
    
        config = ConfigParams.from_tuples(
            "key1.host", "10.1.1.100",
            "key1.port", "8080",
            "key2.host", "10.1.1.100",
            "key2.port", "8082"
        )

        discovery = MemoryDiscovery()
        discovery.configure(config)

        connection = discovery.resolve_one(Context.from_trace_id("123"), "key1")
        # Result: host=10.1.1.100;port=8080
    """

    def __init__(self, config: ConfigParams = None):
        """
        Creates a new instance of discovery service.

        :param config: (optional) configuration with connection parameters.
        """
        self.__items: List[DiscoveryItem] = []
        if not (config is None):
            self.configure(config)

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self.read_connections(config)

    def read_connections(self, connections: ConfigParams):
        """
        Reads connections from configuration parameters.
        Each section represents an individual Connection params

        :param connections: configuration parameters to be read
        """
        self.__items = []

        if len(connections) > 0:
            connection_sections = connections.get_section_names()
            for key in connection_sections:
                value = connections.get_section(key)

                item = DiscoveryItem()
                item.key = key
                item.connection = ConnectionParams(value)
                self.__items.append(item)

    def register(self, context: Optional[IContext], key: str, connection: ConnectionParams) -> ConnectionParams:
        """
        Registers connection parameters into the discovery service.

        :param context: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connection parameters.

        :param connection: a connection to be registered.

        :returns: the registered connection parameters.
        """
        item = DiscoveryItem()
        item.key = key
        item.connection = connection
        self.__items.append(item)
        return connection

    def resolve_one(self, context: Optional[IContext], key: str) -> ConnectionParams:
        """
        Resolves a single connection parameters by its key.

        :param context: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connection.

        :return: a resolved connection.
        """
        connection = None
        for item in self.__items:
            if item.key == key and not (item.connection is None):
                connection = item.connection
                break
        return connection

    def resolve_all(self, context: Optional[IContext], key: str) -> List[ConnectionParams]:
        """
        Resolves all connection parameters by their key.

        :param context: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connections.

        :return: a list with resolved connections.
        """
        connections = []
        for item in self.__items:
            if item.key == key and not (item.connection is None):
                connections.append(item.connection)
        return connections
