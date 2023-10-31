# -*- coding: utf-8 -*-
"""
    pip_services4_container.config.ContainerConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container configuration reader implementation.

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional

from pip_services4_commons.errors import ConfigException
from pip_services4_components.config import ConfigParams
from pip_services4_components.context.IContext import IContext
from pip_services4_config.config import JsonConfigReader, YamlConfigReader

from .ContainerConfig import ContainerConfig


class ContainerConfigReader:
    """
    Helper class that reads container configuration from JSON or YAML file.
    """

    @staticmethod
    def read_from_file(context: Optional[IContext], path: str, parameters: ConfigParams) -> ContainerConfig:
        """
        Reads container configuration from JSON or YAML file.
        The type of the file is determined by file extension.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to component configuration file.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: the read container configuration
        """
        if path is None:
            raise ConfigException(context, "NO_PATH", "Missing config file path")

        index = path.rfind('.')
        ext = path[index + 1:].lower() if index > 0 else ''

        if ext == "json":
            return ContainerConfigReader.read_from_json_file(context, path, parameters)
        elif ext == "yaml" or ext == "yml":
            return ContainerConfigReader.read_from_yaml_file(context, path, parameters)

        # By default read as JSON
        return ContainerConfigReader.read_from_json_file(context, path, parameters)

    @staticmethod
    def read_from_json_file(context: Optional[IContext], path: str, parameters: ConfigParams) -> ContainerConfig:
        """
        Reads container configuration from JSON file.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to component configuration file.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: the read container configuration
        """
        config = JsonConfigReader.read_config(context, path, parameters)
        return ContainerConfig.from_config(config)

    @staticmethod
    def read_from_yaml_file(context: Optional[IContext], path: str, parameters: ConfigParams) -> ContainerConfig:
        """
        Reads container configuration from YAML file.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to component configuration file.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: the read container configuration
        """
        config = YamlConfigReader.read_config(context, path, parameters)
        return ContainerConfig.from_config(config)
