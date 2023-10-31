# -*- coding: utf-8 -*-
"""
    pip_services4_container.refer.RunReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Run references decorator implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, List, Optional

from pip_services4_components.refer import IReferences
from pip_services4_components.run import IOpenable, Opener, Closer
from pip_services4_components.context.IContext import IContext

from .ReferencesDecorator import ReferencesDecorator


class RunReferencesDecorator(ReferencesDecorator, IOpenable):
    """
    References decorator that automatically opens to newly added components
    that implement :class:`IOpenable <pip_services4_commons.run.IOpenable.IOpenable>` interface and closes removed components that implement :class:`IClosable <pip_services4_commons.run.IClosable.IClosable>` interface.
    """

    def __init__(self, next_references: IReferences, top_references: IReferences):
        """
        Creates a new instance of the decorator.

        :param next_references: the next references or decorator in the chain.

        :param top_references: the decorator at the top of the chain.
        """
        super(RunReferencesDecorator, self).__init__(next_references, top_references)
        self._opened = False

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self._opened:
            components = self.get_all()
            Opener.open(context, components)
            self._opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._opened:
            components = self.get_all()
            Closer.close(context, components)
            self._opened = False

    def put(self, locator: Any = None, component: Any = None):
        """
        Puts a new component into this component map.

        :param locator: a locator to find the component by.

        :param component: a component component to be added.
        """
        super(RunReferencesDecorator, self).put(locator, component)

        if self._opened:
            Opener.open_one(None, component)

    def remove(self, locator: Any) -> Any:
        """
        Removes a previously added component that matches specified locator.
        If many references match the locator, it removes only the first one.
        When all references shall be removed, use :func:`removeAll` method instead.

        :param locator: a locator to remove component

        :return: the removed component component.
        """
        component = super(RunReferencesDecorator, self).remove(locator)

        if self._opened:
            Closer.close_one(None, component)

        return component

    def remove_all(self, locator: Any) -> List[Any]:
        """
        Removes all component references that match the specified locator.

        :param locator: the locator to remove references by.

        :return: a list, containing all removed references.
        """
        components = super(RunReferencesDecorator, self).remove_all(locator)

        if self._opened:
            Closer.close(None, components)

        return components
