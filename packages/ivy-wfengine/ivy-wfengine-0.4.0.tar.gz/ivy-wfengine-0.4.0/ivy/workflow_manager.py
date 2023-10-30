# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 4, 2014
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from getopt import getopt
import importlib
import types

from ivy.exceptions.exceptions import InvalidAttributeException
from ivy.utils.utils import TYPE_MAP
from ivy.loop import Loop
from ivy import context
from ivy.utils.struct import Struct
from ivy.backend import SequentialBackend

PLUGINS_KEY = "plugins"
CONTEXT_PROVIDER_KEY = "context_provider"


class WorkflowManager(object):
    """
    Manages the workflow process by loading the passed config and
    parsing the passed arguments and then iterating thru the plugins.
    :param argv: arguments to use
    """

    def __init__(self, argv, **kwargs):
        """
        Constructor
        """
        self._setup(argv, **kwargs)

    def _setup(self, argv, **kwargs):

        config = self._parse_args(argv, **kwargs)

        if PLUGINS_KEY not in config:
            raise InvalidAttributeException("plugins definition is missing")

        if CONTEXT_PROVIDER_KEY in config:

            def get_context_provider_wrapper():
                # TODO: load class not module
                clazz = config[CONTEXT_PROVIDER_KEY]
                module_name = ".".join(clazz.split(".")[:-1])
                module = importlib.import_module(module_name)
                return getattr(module, clazz.split(".")[-1])

            context.get_context_provider = get_context_provider_wrapper

        if not isinstance(config[PLUGINS_KEY], Loop):
            config[PLUGINS_KEY] = Loop(config[PLUGINS_KEY])

        self.ctx = context.create_ctx()
        self.ctx.params = context.create_immutable_ctx(**config)
        # just to maintain backward compatibility
        self.ctx.parameters = self.ctx.params
        self.ctx.plugins = self.ctx.params.plugins

    def _parse_args(self, argv, **kwargs):

        if argv is None or len(argv) < 1:
            raise InvalidAttributeException()

        if isinstance(argv, str):
            argv = [argv]

        if isinstance(argv, dict):
            config = Struct(**argv)
            config.update(**kwargs)
            return config
        else:
            config = load_configs(argv[-1], **kwargs)

        # overwrite parameters by command line options
        optlist, positional = getopt(
            argv, "", [name.replace("_", "-") + "=" for name in config.keys()]
        )
        if len(positional) != 1:
            raise InvalidAttributeException("only one config file is allowed")
        for opt in optlist:
            if opt[0][:2] != "--":
                raise InvalidAttributeException(
                    "invalid option name: {:}".format(opt[0])
                )
            elif not opt[0][2:].replace("-", "_") in config:
                raise InvalidAttributeException(
                    "unknown option: {:}".format(opt[0][2:])
                )
            else:
                name = opt[0][2:].replace("-", "_")

                if name not in kwargs:
                    config[name] = TYPE_MAP[type(config[name]).__name__](opt[1])

        return config

    def launch(self):
        """
        Launches the workflow
        """
        self.ctx.timings = []
        executor = SequentialBackend(self.ctx)
        executor.run(self.ctx.params.plugins)


def load_configs(configs, **kwargs):
    """
    Loads key-value configurations from Python modules.
    :param configs: string or list of strings with absolute module declaration e.g. "ivy.config.base_config
    :param kwargs: keyword arguments which overwrite values in the configurations
    :return config: a :py:class:`Struct` instance with the config attributes
    """

    if configs is None:
        raise InvalidAttributeException("Invalid configuration passed")

    if not isinstance(configs, list):
        configs = [configs]

    if len(configs) < 1:
        raise InvalidAttributeException("Invalid configuration passed")

    args = {}
    for config_name in configs:
        config = importlib.reload(importlib.import_module(config_name))

        attrs = []
        for name in dir(config):
            if not name.startswith("__"):
                attr = getattr(config, name)
                if not isinstance(attr, types.ModuleType):
                    attrs.append((name, attr))

        args.update(attrs)

    args.update(kwargs)

    return Struct(**args)
