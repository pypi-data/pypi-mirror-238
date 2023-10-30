# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 18, 2014
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals
from multiprocessing import Pool
import time
from ivy.context import get_context_provider
from ivy.utils.timing import SimpleTiming
from ivy.utils.timing import TimingCollection


class SimpleMapPlugin(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def get_workload(self):
        return [self.ctx]


class SequentialBackend(object):
    """
    Simple implementation of a backend executing the plugins in a sequential order
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def run(self, loop, map_plugin=None):

        if map_plugin is None:
            map_plugin = SimpleMapPlugin(self.ctx)

        return list(map(LoopWrapper(loop), map_plugin.get_workload()))


class MultiprocessingBackend(object):
    """
    Backend based on Python's multiprocessing.
    Will instantiate a multiprocessing pool with ``ctx.params.cpu_count`` processes.
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def run(self, loop, map_plugin):
        pool = Pool(self.ctx.params.cpu_count)
        try:
            ctx_list = pool.map(LoopWrapper(loop, True), map_plugin.get_workload())
            timing_collection = TimingCollection(str(loop))
            for ctx in ctx_list:
                for timing in ctx.timings:
                    timing_collection.add_timing(timing)
            self.ctx.timings.append(timing_collection)
            return ctx_list
        finally:
            pool.close()


class IpClusterBackend(object):
    """
    Backend based on IPython cluster.
    Will distribute the workload among the available engines.
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def run(self, loop, map_plugin):
        from IPython import parallel

        client = parallel.Client()
        view = client.load_balanced_view()
        try:
            return view.map_sync(LoopWrapper(loop), map_plugin.get_workload())
        finally:
            pass


#             view.close()


class JoblibBackend(object):
    """
    Backend based on the joblib package
    Will instantiate a multiprocessing pool with ``ctx.params.cpu_count`` processes.
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def run(self, loop, map_plugin):
        import joblib

        with joblib.Parallel(n_jobs=self.ctx.params.cpu_count) as parallel:
            ctx_list = parallel(
                joblib.delayed(LoopWrapper(loop, True), False)(ctx)
                for ctx in map_plugin.get_workload()
            )
            timing_collection = TimingCollection(str(loop))
            for ctx in ctx_list:
                for timing in ctx.timings:
                    timing_collection.add_timing(timing)
            self.ctx.timings.append(timing_collection)
            return ctx_list


class LoopWrapper(object):
    """
    Callable wrapper for the loop execution
    """

    def __init__(self, loop, parallel=False):
        self.loop = loop
        self.parallel = parallel

    def __call__(self, ctx):

        if self.parallel:
            ctx.timings = []

        self.loop.set_context(ctx)

        for plugin in self.loop:
            start = time.time()
            plugin()
            ctx.timings.append(SimpleTiming(str(plugin), time.time() - start))

            get_context_provider().store_context(ctx)

        self.loop.reset()

        return ctx


BACKEND_NAME_MAP = {
    "sequential": SequentialBackend,
    "multiprocessing": MultiprocessingBackend,
    "ipcluster": IpClusterBackend,
    "joblib": JoblibBackend,
}


def create(ctx, force=None):
    """
    Simple factory instantiating backends for the given name in ``ctx.params.backend``
    """
    backend_name = ctx.params.backend if force is None else force
    return BACKEND_NAME_MAP[backend_name](ctx)
