# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.WorkflowManager` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from operator import eq

import pytest

from getopt import GetoptError
from ivy.loop import Loop
from ivy.workflow_manager import WorkflowManager, load_configs
from ivy.exceptions.exceptions import InvalidAttributeException


def test_launch_from_list():
    args = ["tests.config.workflow_config"]

    mgr = WorkflowManager(args)
    mgr.launch()

    assert mgr.ctx is not None
    assert mgr.ctx.params is not None
    assert mgr.ctx.params.plugins is not None


def test_launch_from_string():
    args = "tests.config.workflow_config"

    mgr = WorkflowManager(args)
    mgr.launch()

    assert mgr.ctx is not None
    assert mgr.ctx.params is not None
    assert mgr.ctx.params.plugins is not None


def test_parse_args():
    args = [
        "--a=True",
        "--b=False",
        "--c=-1",
        "--d=0",
        "--e=1",
        "--f=-1.0",
        "--g=0.0",
        "--h=1.0",
        "--i=le_string",
        "--j=1,2,3,4",
        "--bool1=True",
        "--bool2=False",
        "--bool3=True",
        "--bool4=False",
        "tests.config.workflow_config",
    ]

    mgr = WorkflowManager(args)

    assert mgr.ctx.params.a
    assert not mgr.ctx.params.b
    assert mgr.ctx.params.c == -1
    assert mgr.ctx.params.d == 0
    assert mgr.ctx.params.e == 1
    assert mgr.ctx.params.f == -1.0
    assert mgr.ctx.params.g == 0.0
    assert mgr.ctx.params.h == 1.0
    assert mgr.ctx.params.i == "le_string"
    assert mgr.ctx.params.bool1
    assert not mgr.ctx.params.bool2
    assert mgr.ctx.params.bool3
    assert not mgr.ctx.params.bool4
    assert all(map(eq, mgr.ctx.params.j, [1, 2, 3, 4]))


def test_parse_args_and_kwargs():
    args = [
        "--a=True",
        "--b=False",
        "--c=-1",
        "--d=0",
        "--e=1",
        "--f=-1.0",
        "--g=0.0",
        "--h=1.0",
        "--i=le_string",
        "--j=1,2,3,4",
        "--bool1=True",
        "--bool2=False",
        "--bool3=True",
        "--bool4=False",
        "tests.config.workflow_config",
    ]

    mgr = WorkflowManager(args, d=3.412, i="other_string", bool2=True, j=(1, 2, 3))

    assert mgr.ctx.params.a
    assert not mgr.ctx.params.b
    assert mgr.ctx.params.c == -1
    assert mgr.ctx.params.d == 3.412
    assert mgr.ctx.params.e == 1
    assert mgr.ctx.params.f == -1.0
    assert mgr.ctx.params.g == 0.0
    assert mgr.ctx.params.h == 1.0
    assert mgr.ctx.params.i == "other_string"
    assert mgr.ctx.params.bool1
    assert mgr.ctx.params.bool2
    assert mgr.ctx.params.bool3
    assert not mgr.ctx.params.bool4
    assert mgr.ctx.params.j == (1, 2, 3)


def test_simple_launch():
    args = ["tests.config.workflow_config_simple"]

    mgr = WorkflowManager(args)
    mgr.launch()

    assert mgr.ctx is not None
    assert mgr.ctx.params is not None
    assert mgr.ctx.params.plugins is not None
    assert isinstance(mgr.ctx.params.plugins, Loop)


def test_missing_plugins():

    args = ["ivy.config.base_config"]

    with pytest.raises(InvalidAttributeException):
        WorkflowManager(args)


def test_missing_config():

    with pytest.raises(InvalidAttributeException):
        WorkflowManager(None)

    with pytest.raises(InvalidAttributeException):
        WorkflowManager([])


def test_invalid_config():

    args = [
        "tests.config.workflow_config_simple",
        "tests.config.workflow_config_simple",
    ]

    with pytest.raises(InvalidAttributeException):
        WorkflowManager(args)


def test_invalid_args():

    args = ["-a=1", "tests.config.workflow_config_simple"]

    with pytest.raises(GetoptError):
        WorkflowManager(args)


def test_unknown_args():

    args = ["--a=1", "tests.config.workflow_config_simple"]

    with pytest.raises(GetoptError):
        WorkflowManager(args)


def test_loop():
    args = ["tests.config.workflow_config"]
    mgr = WorkflowManager(args)
    mgr.launch()
    assert len(mgr.ctx.timings) == 2


def test_load_configs_invalid():
    with pytest.raises(InvalidAttributeException):
        load_configs(None)


def test_load_configs_one_arg():
    config = load_configs("tests.config.workflow_config_args")
    assert config is not None
    assert config.conf_arg_int == 1
    assert config.conf_arg_float == 1.0
    assert config.conf_arg_str == "1"


def test_load_configs_one_arg_and_kwargs():
    config = load_configs(
        "tests.config.workflow_config_args", conf_arg_str="string", alpha=6.7
    )
    assert config is not None
    assert config.conf_arg_int == 1
    assert config.conf_arg_float == 1.0
    assert config.conf_arg_str == "string"
    assert config.alpha == 6.7


def test_load_configs_multiple_arg():

    config = load_configs(
        ["tests.config.workflow_config_args", "tests.config.workflow_config"]
    )
    assert config is not None

    # from workflow_config_args
    assert config.conf_arg_int == 1
    assert config.conf_arg_float == 1.0
    assert config.conf_arg_str == "1"

    # from workflow_config
    assert config.a is None
    assert config.b is None


def test_load_configs_multiple_arg_and_kwargs():

    config = load_configs(
        ["tests.config.workflow_config_args", "tests.config.workflow_config"],
        new=1,
        h=4,
    )
    assert config is not None

    # from workflow_config_args
    assert config.conf_arg_int == 1
    assert config.conf_arg_float == 1.0
    assert config.conf_arg_str == "1"

    # from workflow_config
    assert config.a is None
    assert config.b is None

    # from kwargs
    assert config.new == 1
    assert config.h == 4


def test_load_configs_overwrite():

    config = load_configs("tests.config.workflow_config_args")

    assert config is not None
    assert config.conf_arg_int == 1

    config.conf_arg_int = 2
    assert config.conf_arg_int == 2


def test_create_from_dict():
    args = {
        "plugins": ["tests.plugin.simple_plugin", "tests.plugin.simple_plugin"],
        "a": 1,
    }

    mgr = WorkflowManager(args)
    assert mgr.ctx.params is not None
    assert mgr.ctx.params.a is 1
    assert mgr.ctx.params.plugins is not None
    assert len(mgr.ctx.params.plugins.pluginList) == 2


def test_create_from_dict_and_kwargs():
    args = {
        "plugins": ["tests.plugin.simple_plugin", "tests.plugin.simple_plugin"],
        "a": 1,
    }

    mgr = WorkflowManager(args, a=2, b=None)
    assert mgr.ctx.params is not None
    assert mgr.ctx.params.a is 2
    assert mgr.ctx.params.b is None
    assert mgr.ctx.params.plugins is not None
    assert len(mgr.ctx.params.plugins.pluginList) == 2
