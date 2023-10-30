# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 18, 2014

author: jakeret
"""

from __future__ import print_function, division, absolute_import
from ivy.plugin.base_plugin import BasePlugin
from ivy.loop import Loop
from ivy.plugin.plugin_factory import PluginFactory
from ivy.exceptions.exceptions import InvalidAttributeException
from ivy import backend


class ParallelPluginCollection(BasePlugin):
    """
    Collection that allows for executing plugins in parallel by using
    a MapReduce aprach. The implementation therefore requires a
    list of plugins to execute, a map plugin creating the workload and
    (optionally) a reduce plugin reducing the data from the parallel task exection

    :param plugin_list: List of plugins (or a Loop) which should be executed in parallel
    :param map_plugin:
    :param reduce_plugin: (optional)
    :param ctx: (optional)
    """

    def __init__(
        self, plugin_list, map_plugin, reduce_plugin=None, ctx=None, parallel=True
    ):
        """
        Constructor
        """

        self.ctx = ctx

        if self.ctx is not None:
            super(ParallelPluginCollection, self).__init__(self.ctx)

        if not isinstance(plugin_list, Loop):
            plugin_list = Loop(plugin_list, ctx=self.ctx)

        self.pluginList = plugin_list

        if map_plugin is None:
            raise InvalidAttributeException("No map plugin provided")

        self.mapPlugin = map_plugin
        self.reducePlugin = reduce_plugin
        self.parallel = parallel

    def __str__(self):
        return "ParallelPluginCollection"

    def __call__(self):
        force = None
        if not self.parallel:
            force = "sequential"

        backend_impl = backend.create(self.ctx, force)

        map_plugin = self.mapPlugin
        if isinstance(self.mapPlugin, str):
            map_plugin = PluginFactory.create_instance(map_plugin, self.ctx)

        ctx_list = backend_impl.run(self.pluginList, map_plugin)

        if self.reducePlugin is not None:
            reduce_plugin = self.reducePlugin
            if isinstance(self.reducePlugin, str):
                reduce_plugin = PluginFactory.create_instance(reduce_plugin, self.ctx)

            reduce_plugin.reduce(ctx_list)
