# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.simple_plugin` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from tests.plugin.simple_plugin import Plugin
from ivy import context


class TestSimplePlugin(object):
    def test_simple(self):

        ctx = context.create_ctx()

        plugin = Plugin(ctx)
        assert plugin.value is None

        plugin = Plugin(ctx, value=1)
        assert plugin.value == 1

        Plugin(ctx, foo=1)
        assert ctx.foo == 1
