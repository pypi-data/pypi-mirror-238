# -*- coding: utf-8 -*-
"""
    pip_services4_config.config.YamlConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    YAML config reader implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os.path
from typing import Any, Optional

import yaml
from pip_services4_commons.errors.ConfigException import ConfigException
from pip_services4_commons.errors.FileException import FileException
from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext
from pip_services4_components.context.ContextResolver import ContextResolver

from .FileConfigReader import FileConfigReader


class YamlConfigReader(FileConfigReader):
    """
    Config reader that reads configuration from YAML file.

    ### Configuration parameters ###

        - path:          path to configuration file
        - parameters:    this entire section is used as template parameters
        - ...

    Example:

    .. code-block:: yml
    
        ======== config.yml ======
        key1: "{{KEY1_VALUE}}"
        key2: "{{KEY2_VALUE}}"
        ===========================

    .. code-block:: python
    
        configReader = YamlConfigReader("config.yml")
        parameters = ConfigParams.from_tuples("KEY1_VALUE", 123, "KEY2_VALUE", "ABC")
        configReader.read_config_(Context.from_trace_id("123"), parameters)
    """

    def __init__(self, path: str = None):
        """
        Creates a new instance of the config reader.

        :param path: (optional) a path to configuration file.
        """
        super(YamlConfigReader, self).__init__(path)

    def _read_object(self, context: Optional[IContext], parameters: ConfigParams) -> Any:
        """
        Reads configuration file, parameterizes its content and converts it into YAML object.

        :param context: (optional) transaction id to trace execution through call chain.

        :param parameters: values to parameters the configuration.

        :return: a YAML object with configuration.
        """
        path = self.get_path()

        if path is None:
            raise ConfigException(ContextResolver.get_trace_id(context), "NO_PATH", "Missing config file path")

        if not os.path.isfile(path):
            raise FileException(ContextResolver.get_trace_id(context), 'FILE_NOT_FOUND', 'Config file was not found at ' + path)

        try:
            with open(path, 'r') as file:
                config = file.read()
                config = self._parameterize(config, parameters)
                return yaml.load(config, Loader=yaml.FullLoader)
        except Exception as ex:
            raise FileException(
                ContextResolver.get_trace_id(context),
                "READ_FAILED",
                "Failed reading configuration " + path + ": " + str(ex)
            ).with_details("path", path).with_cause(ex)

    def read_config_(self, context: Optional[IContext], parameters: ConfigParams) -> ConfigParams:
        """
        Reads configuration and parameterize it with given values.

        :param context: (optional) transaction id to trace execution through call chain.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: ConfigParams configuration.
        """
        value = self._read_object(context, parameters)
        return ConfigParams.from_value(value)

    @staticmethod
    def read_object(context: Optional[IContext], path: str, parameters: ConfigParams) -> Any:
        """
        Reads configuration file, parameterizes its content and converts it into YAML object.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to configuration file.

        :param parameters: values to parameters the configuration.

        :return: a YAML object with configuration.
        """
        return YamlConfigReader(path)._read_object(context, parameters)

    @staticmethod
    def read_config(context: Optional[IContext], path: str, parameters: ConfigParams) -> ConfigParams:
        """
        Reads configuration from a file, parameterize it with given values and returns a new ConfigParams object.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to configuration file.

        :param parameters: values to parameters the configuration.

        :return: ConfigParams configuration.
        """
        value = YamlConfigReader(path)._read_object(context, parameters)
        return ConfigParams.from_value(value)
