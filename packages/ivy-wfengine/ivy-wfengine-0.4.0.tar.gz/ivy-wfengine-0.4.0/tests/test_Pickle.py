# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.loop ` module.

author: jakeret
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from pickle import dumps
from pickle import loads

from ivy import context
from ivy.loop import Loop
from ivy.plugin.parallel_plugin_collection import ParallelPluginCollection
from ivy.utils.struct import Struct
from ivy.workflow_manager import WorkflowManager
from ivy.loop import ListIter


PLUGIN_NAME = "tests.plugin.simple_plugin"


class TestPickle(object):
    def test_loop_pickle(self):

        ctx = context.create_ctx()
        loop = Loop([PLUGIN_NAME, PLUGIN_NAME], ctx=ctx)
        loop.next()

        s_loop = dumps(loop)
        loop2 = loads(s_loop)

        for p in loop2:
            p()

        loop.reset()

        s_loop = dumps(loop)
        loop2 = loads(s_loop)

        for p in loop2:
            p()

    def test_struct_pickle(self):
        struct = Struct(value1=1)
        struct.params = Struct(backend="multiprocessing")
        loads(dumps(struct))

    def test_parallel_plugin_collection_pickle(self):

        parallel_plugin_collection = ParallelPluginCollection(
            "ivy.plugin.simple_map_plugin",
            ["ivy.plugin.simple_square_plugin"],
            "ivy.plugin.simple_reduce_plugin",
        )

        loads(dumps(parallel_plugin_collection))

    def test_context_pickle(self):
        ctx = context.create_ctx()
        loads(dumps(ctx))

    def test_workflow_context_pickle(self):

        args = [
            "--backend=multiprocessing",
            "--cpu-count=1",
            "tests.config.workflow_config_parallel",
        ]

        mgr = WorkflowManager(args)
        loads(dumps(mgr.ctx))

    def test_list_iter_pickle(self):

        list_iter = ListIter(["a", "b", "c"])
        next(list_iter)

        for _ in loads(dumps(list_iter)):
            pass
