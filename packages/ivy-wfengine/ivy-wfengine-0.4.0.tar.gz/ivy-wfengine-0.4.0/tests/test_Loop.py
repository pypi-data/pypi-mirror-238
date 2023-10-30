# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.Loop` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import
import pytest

from ivy import context
from ivy.loop import Loop
from ivy.exceptions.exceptions import InvalidLoopException
from tests.plugin.simple_plugin import Plugin
from ivy.exceptions.exceptions import UnsupportedPluginTypeException
from ivy.context import loop_ctx
from ivy.utils.stop_criteria import RangeStopCriteria


PLUGIN_NAME = "tests.plugin.simple_plugin"
CTX = context.create_ctx()


class TestLoop(object):
    def test_none(self):
        with pytest.raises(InvalidLoopException):
            Loop(None)

    def test_register(self):

        loop = Loop(PLUGIN_NAME)

        with pytest.raises(TypeError):
            loop.next()
            loop()

        loop.set_context(CTX)
        assert loop in CTX

    def test_one_plugin(self):

        plugin = Plugin(CTX)
        loop = Loop(plugin, ctx=CTX)

        p = loop.next()
        assert p == plugin
        assert p.ctx == CTX

        with pytest.raises(StopIteration):
            loop.next()

    def test_plugin_instances(self):

        plugin1 = Plugin(CTX)
        plugin2 = Plugin(CTX)
        loop = Loop([plugin1, plugin2], ctx=CTX)

        p = loop.next()
        assert p == plugin1
        p = loop.next()
        assert p == plugin2

        with pytest.raises(StopIteration):
            loop.next()

    def test_plugin_names(self):

        loop = Loop([PLUGIN_NAME, PLUGIN_NAME], ctx=CTX)

        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX
        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX

        with pytest.raises(StopIteration):
            loop.next()

    def test_inner_loop(self):

        loop = Loop(Loop([PLUGIN_NAME, PLUGIN_NAME]), ctx=CTX)

        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX
        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX

        with pytest.raises(StopIteration):
            loop.next()

    def test_complex_loop(self):

        loop = Loop(
            [PLUGIN_NAME, Loop([PLUGIN_NAME, PLUGIN_NAME]), PLUGIN_NAME], ctx=CTX
        )

        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX
        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX
        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX
        p = loop.next()
        assert isinstance(p, Plugin)
        assert p.ctx == CTX

        with pytest.raises(StopIteration):
            loop.next()

    def test_loop_iter(self):

        plugin_list = [PLUGIN_NAME, PLUGIN_NAME]
        loop = Loop(plugin_list, ctx=CTX)

        cnt = 0
        for p in loop:
            assert isinstance(p, Plugin)
            assert p.ctx == CTX
            cnt += 1

        assert cnt == len(plugin_list)

    def test_loop_max_iter(self):

        max_iter = 3
        plugin_list = [PLUGIN_NAME, PLUGIN_NAME]

        loop = Loop(plugin_list, ctx=CTX, stop=RangeStopCriteria(max_iter=max_iter))

        cnt = 0
        for p in loop:
            assert isinstance(p, Plugin)
            assert p.ctx == CTX
            cnt += 1

        assert cnt == len(plugin_list) * max_iter

    def test_loop_max_iter_nested(self):

        max_iter = 3
        plugin_list = [Plugin(CTX), Plugin(CTX)]

        loop = Loop(
            Loop(plugin_list, stop=RangeStopCriteria(max_iter=max_iter)),
            ctx=CTX,
            stop=RangeStopCriteria(max_iter=max_iter),
        )

        cnt = 0
        for p in loop:
            assert isinstance(p, Plugin)
            assert p.ctx == CTX
            p()
            cnt += 1

        assert cnt == len(plugin_list) * max_iter * max_iter

    def test_loop_ctx(self):

        loop = Loop(PLUGIN_NAME)

        with pytest.raises(TypeError):
            loop_ctx(loop)

        loop.ctx = CTX

        with pytest.raises(KeyError):
            loop_ctx(loop)

        loop.set_context(CTX)
        loop_ctx(loop)

    def test_unknown_plugin(self):

        plugin = "unknown.plugin.invalid"
        loop = Loop(plugin, ctx=CTX)

        with pytest.raises(UnsupportedPluginTypeException):
            loop.next()

        plugin = {}
        loop = Loop(plugin, ctx=CTX)

        with pytest.raises(UnsupportedPluginTypeException):
            loop.next()
