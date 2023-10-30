# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.plugin.plugin_factory ` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from ivy import context
from ivy.exceptions.exceptions import UnsupportedPluginTypeException
from ivy.plugin.plugin_factory import PluginFactory
from tests.plugin import simple_plugin

PLUGIN_NAME = "tests.plugin.simple_plugin"
CTX = context.create_ctx()


class TestPluginFactory(object):
    def test_simple(self):
        plugin = PluginFactory.create_instance(PLUGIN_NAME, CTX)
        assert plugin is not None
        assert isinstance(plugin, simple_plugin.Plugin)

    def test_unknown_module(self):

        plugin_name = "unknown.plugin.invalid"

        with pytest.raises(UnsupportedPluginTypeException):
            PluginFactory.create_instance(plugin_name, CTX)

    def test_invalid_module(self):

        plugin_name = "ivy.plugin.BasePlugin"

        with pytest.raises(UnsupportedPluginTypeException):
            PluginFactory.create_instance(plugin_name, CTX)
