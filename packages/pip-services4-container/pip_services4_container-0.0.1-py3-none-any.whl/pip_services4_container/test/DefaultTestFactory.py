# -*- coding: utf-8 -*-

from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .Shutdown import Shutdown


class DefaultTestFactory(Factory):
    """
    Creates test components by their descriptors.

    See :class:`Factory <pip_services4_components.build.Factory.Factory>`,
    :class:`Shutdown <pip_services4_components.test.Shutdown.Shutdown>`
    """
    ShutdownDescriptor = Descriptor("pip-services", "shutdown", "*", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultTestFactory, self).__init__()
        self.register_as_type(DefaultTestFactory.ShutdownDescriptor, Shutdown)
