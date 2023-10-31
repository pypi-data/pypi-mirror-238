# -*- coding: utf-8 -*-
"""
    pip_services4_container.build.DefaultContainerFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default container factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import CompositeFactory, IFactory
from pip_services4_components.context import DefaultContextFactory
from pip_services4_config.build import DefaultConfigFactory
from pip_services4_logic.build.DefaultLogicFactory import DefaultLogicFactory

from pip_services4_container.test import DefaultTestFactory
from pip_services4_observability.build.DefaultObservabilityFactory import DefaultObservabilityFactory


class DefaultContainerFactory(CompositeFactory):
    """
    Creates default container components (loggers, counters, caches, locks, etc.) by their descriptors.
    """

    def __init__(self, *factories: IFactory):
        """
        Create a new instance of the factory and sets nested factories.

        :param factories: a list of nested factories
        """
        super(DefaultContainerFactory, self).__init__(*factories)
        self.add(DefaultContextFactory())
        self.add(DefaultObservabilityFactory())
        self.add(DefaultLogicFactory())
        self.add(DefaultConfigFactory())
        self.add(DefaultTestFactory())
