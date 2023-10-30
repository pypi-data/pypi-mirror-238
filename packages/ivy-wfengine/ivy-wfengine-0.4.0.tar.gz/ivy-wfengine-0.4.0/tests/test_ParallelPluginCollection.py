# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.plugin.parallel_plugin_collection ` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from ivy import context
from ivy.workflow_manager import WorkflowManager
from ivy.exceptions.exceptions import InvalidAttributeException, InvalidLoopException
from ivy.plugin.parallel_plugin_collection import ParallelPluginCollection
from tests.plugin import range_map_plugin
from tests.plugin import sum_reduce_plugin

PLUGIN_NAME = "tests.plugin.simple_square_plugin"


class TestParallelPluginCollection(object):
    def test_setup(self):

        with pytest.raises(InvalidLoopException):
            ParallelPluginCollection(None, "tests.plugin.range_map_plugin")

        with pytest.raises(InvalidAttributeException):
            ParallelPluginCollection([], None)

    def test_sequential(self):

        ctx = context.create_ctx()
        ctx.timings = []
        ctx.params = context.create_immutable_ctx(
            backend="sequential", valuesMin=1, valuesMax=10
        )

        map_plugin = range_map_plugin.Plugin(ctx)
        plugin_list = [PLUGIN_NAME]
        reduce_plugin = sum_reduce_plugin.Plugin(ctx)

        parallel_plugin_collection = ParallelPluginCollection(
            plugin_list, map_plugin, reduce_plugin, ctx=ctx
        )
        parallel_plugin_collection()
        assert ctx.valuesSum == 285

    def test_multiprocessing(self):

        ctx = context.create_ctx()
        ctx.timings = []
        ctx.params = context.create_immutable_ctx(
            backend="multiprocessing", cpu_count=8, valuesMin=1, valuesMax=10
        )

        map_plugin = range_map_plugin.Plugin(ctx)
        plugin_list = [PLUGIN_NAME]
        reduce_plugin = sum_reduce_plugin.Plugin(ctx)

        parallel_plugin_collection = ParallelPluginCollection(
            plugin_list, map_plugin, reduce_plugin, ctx=ctx
        )
        parallel_plugin_collection()
        assert ctx.valuesSum == 285

    def test_parallel_workflow(self):

        args = [
            "--backend=multiprocessing",
            "--cpu-count=1",
            "tests.config.workflow_config_parallel",
        ]

        mgr = WorkflowManager(args)
        mgr.launch()
        assert mgr.ctx.valuesSum == 285
