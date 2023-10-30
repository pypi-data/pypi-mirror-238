# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 4, 2014
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from ivy import context
from ivy.exceptions.exceptions import InvalidLoopException
from ivy.exceptions.exceptions import UnsupportedPluginTypeException
from ivy.plugin.base_plugin import BasePlugin
from ivy.plugin.plugin_factory import PluginFactory
from ivy.utils.stop_criteria import SimpleStopCriteria
from ivy.utils.struct import WorkflowState
from ivy.utils.utils import ListIter


class Loop(object):
    """
    Implementation of a loop.

    :param pluginList: List of plugin or inner :class:`Loop`
    :param stop: (optional) stop criteria
    """

    _currentPlugin = None

    def __init__(self, plugin_list, ctx=None, stop=None):

        self.ctx = None
        if ctx is not None:
            self.set_context(ctx)

        if plugin_list is None:
            raise InvalidLoopException("Plugin list is None")

        if not isinstance(plugin_list, list):
            plugin_list = [plugin_list]

        self.pluginList = plugin_list
        self._create_iter()

        if stop is None:
            stop = self._create_stop_criteria()

        stop.parent = self
        self._stopCriteria = stop

    def set_context(self, ctx):

        self.ctx = ctx

        if self not in self.ctx:
            context.register(self)

    def reset(self):
        """
        Resets the internal state of the loop
        """
        self.plugin_list_itr = ListIter(self.pluginList)
        context.loop_ctx(self).reset()

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns the next plugin. Allows for using a Loop as an iter
        """
        # self.register()

        try:
            if self._stopCriteria.is_stop():
                raise StopIteration

            if self._currentPlugin is None:
                self._currentPlugin = self.plugin_list_itr.__next__()

                plugin = self._currentPlugin
                if isinstance(plugin, BasePlugin):
                    print("ITS A BASE PLUGIN")
                    self._currentPlugin = None
                    plugin.ctx = self.ctx
                    return plugin

                if isinstance(plugin, str):
                    self._currentPlugin = None
                    return self._instantiate(plugin)

            if isinstance(self._currentPlugin, Loop):

                inner_loop = self._currentPlugin
                inner_loop.set_context(self.ctx)

                try:
                    plugin = inner_loop.__next__()
                    return plugin
                except StopIteration:
                    if context.loop_ctx(inner_loop).state == WorkflowState.EXIT:
                        raise StopIteration

                    # inner
                    context.loop_ctx(inner_loop).reset()
                    self._currentPlugin = None
                    return self.__next__()

            else:
                raise UnsupportedPluginTypeException()

        except StopIteration:
            context.loop_ctx(self).increment()
            self._create_iter()

            if self._stopCriteria.is_stop():
                raise StopIteration
            else:
                return self.__next__()

    next = __next__  # python 2

    def __call__(self):
        """
        Executes all the plugins sequentially in the loop
        """
        for plugin in self:
            plugin()

    def __setstate__(self, state):
        self.__dict__ = state

    def _create_stop_criteria(self):
        return SimpleStopCriteria()

    def _instantiate(self, plugin_name):
        return PluginFactory.create_instance(plugin_name, self.ctx)

    def _load_iter(self):
        if self.plugin_list_itr is None:
            self._create_iter()

    def _create_iter(self):
        self.plugin_list_itr = ListIter(self.pluginList)
