# -*- coding: utf-8 -*-
"""
    pip_services4_container.Container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container implementation.

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback
from typing import Optional

from pip_services4_commons.errors import InvalidStateException
from pip_services4_components.build import IFactory
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import ContextInfo, DefaultContextFactory
from pip_services4_components.refer import IReferenceable, IUnreferenceable, IReferences, Descriptor
from pip_services4_components.context.IContext import IContext
from pip_services4_components.run import IOpenable
from pip_services4_observability.log import ILogger, NullLogger, CompositeLogger

from pip_services4_container.build.DefaultContainerFactory import DefaultContainerFactory
from pip_services4_container.config.ContainerConfig import ContainerConfig
from pip_services4_container.config.ContainerConfigReader import ContainerConfigReader
from pip_services4_container.refer.ContainerReferences import ContainerReferences


class Container(IConfigurable, IReferenceable, IUnreferenceable, IOpenable):
    """
    Inversion of control (IoC) container that creates components and manages their lifecycle.

    The container is driven by configuration, that usually stored in JSON or YAML file.
    The configuration contains a list of components identified by type or locator, followed by component configuration.

    On container start it performs the following actions:
        - Creates components using their types or calls registered factories to create components using their locators
        - Configures components that implement IConfigurable interface and passes them their configuration parameters
        - Sets references to components that implement IReferenceable interface and passes them references of all components in the container
        - Opens components that implement IOpenable interface

    On container stop actions are performed in reversed order:
        - Closes components that implement ICloseable interface
        - Unsets references in components that implement IUnreferenceable interface
        - Destroys components in the container.

    The component configuration can be parameterized by dynamic values. That allows specialized containers
    to inject parameters from command line or from environment variables.

    The container automatically creates a ContextInfo component that carries detail information
    about the container and makes it available for other components.

    ### Configuration parameters ###
        - name: 					the context (container or process) name
        - description: 		   	human-readable description of the context
        - properties: 			    entire section of additional descriptive properties
        - ...

        Example:

        .. code-block:: yaml

            ======= config.yaml ========
            - descriptor: mygroup:mycomponent1:default:default:1.0
            param1: 123
            param2: ABC

            - type: mycomponent2,mypackage
            param1: 321
            param2: XYZ
            ============================

        .. code-block:: python

            container = Container()
            container.add_factory(MyComponentFactory())

            parameters = ConfigParams.from_value(os.env)
            container.read_config_from_file(Context.from_trace_id("123"), "./config/config.yml", parameters)

            container.open(Context.from_trace_id("123"))
            print "Container is opened"
            # process...
            container.close(Context.from_trace_id("123"))
            print "Container is closed"
    """

    def __init__(self, name: str = None, description: str = None):
        """
        Creates a new instance of the container.

        :param name: (optional) a container name (accessible via ContextInfo)

        :param description: (optional) a container description (accessible via ContextInfo)
        """

        self._config: ContainerConfig = None
        self._references: ContainerReferences = None
        self._logger: ILogger = NullLogger()
        self._info: ContextInfo = ContextInfo(name, description)
        self._factories: DefaultContainerFactory = DefaultContainerFactory()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._config = ContainerConfig.from_config(config)

    def read_config_from_file(self, context: Optional[IContext], path: str, parameters: ConfigParams):
        """
        Reads container configuration from JSON or YAML file and parameterizes it with given values.

        :param context: (optional) transaction id to trace execution through call chain.

        :param path: a path to configuration file

        :param parameters: values to parameters the configuration or null to skip parameterization.
        """
        self._config = ContainerConfigReader.read_from_file(context, path, parameters)
        self._logger.trace(context, self._config.__str__())

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        pass

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        pass

    def __init_references(self, references: IReferences):
        # Override in base classes
        existingInfo = references.get_one_optional(DefaultContextFactory.ContextInfoDescriptor)
        if existingInfo is None:
            references.put(DefaultContextFactory.ContextInfoDescriptor, self._info)
        else:
            self._info = existingInfo
        references.put(Descriptor("pip-services", "factory", "container", "default", "1.0"), self._factories)

    def add_factory(self, factory: IFactory):
        """
        Adds a factory to the container. The factory is used to create components
        added to the container by their locators (descriptors).

        :param factory: a component factory to be added.
        """
        self._factories.add(factory)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._references is not None

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._references is not None:
            raise InvalidStateException(context, "ALREADY_OPENED", "Container was already opened")

        try:
            self._logger.trace(context, "Starting container.")

            # Create references with configured components
            self._references = ContainerReferences()
            self.__init_references(self._references)
            self._references.put_from_config(self._config)
            self.set_references(self._references)

            # Get custom description if available
            info_descriptor = Descriptor("*", "context-info", "*", "*", "*")
            self._info = self._references.get_one_optional(info_descriptor)

            # Reference and open components
            self._references.open(context)

            # Get component to logger
            self._logger = CompositeLogger(self._references)
            self._logger.info(context, "Container " + self._info.name + " started.")
        except Exception as ex:
            self._logger.fatal(context, ex, "Failed to start container")

            self.close(None)

            traceback.print_exc()
            raise ex

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._references is None:
            return

        try:
            self._logger.trace(context, "Stopping " + self._info.name + " container")

            # Unset references for child container
            self.unset_references()

            # Close and deference components
            self._references.close(context)
            self._references = None

            self._logger.info(context, "Container " + self._info.name + " stopped")
        except Exception as ex:
            self._logger.error(context, ex, "Failed to stop container")
            raise ex
