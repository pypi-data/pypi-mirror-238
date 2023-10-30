# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 5, 2014

author: jakeret
"""

import importlib
from ivy.exceptions.exceptions import UnsupportedPluginTypeException


class PluginFactory(object):
    """
    Simple factory creating instances of plugins
    """

    @staticmethod
    def create_instance(plugin_name, ctx):
        """
        Instantiates the given plugin. Expects that the given module contains a class
        with the name 'Plugin'
        :param plugin_name: name of the plugin to instanciate
        :param ctx: context
        :return plugin: an instance of the plugin
        :raises: UnsupportedPluginTypeException
        """

        try:
            module = importlib.import_module(plugin_name)
            plugin = module.Plugin(ctx)
            return plugin
        except ImportError as ex:
            raise UnsupportedPluginTypeException(
                "Module '%s' could not be loaded" % plugin_name, ex
            )
        except AttributeError:
            raise UnsupportedPluginTypeException(
                "Module '%s' has no class definition 'Plugin(ctx)'" % plugin_name
            )

        except Exception as ex:
            raise UnsupportedPluginTypeException(
                "Module '%s' could not be instantiated'" % plugin_name, ex
            )
