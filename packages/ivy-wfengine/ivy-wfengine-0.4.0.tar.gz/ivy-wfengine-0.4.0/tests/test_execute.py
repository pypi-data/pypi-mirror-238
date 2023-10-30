# Copyright (C) 2018 ETH Zurich, Institute for Particle Physics and Astrophysics

"""
Created on Oct 31, 2018
author: Joerg Herbel

Tests the execute function defined in ivy.__init__. Also checks if multiple executes in the same python program yield
the expected result.
"""

from ivy import execute


def test_execute():
    exp_value_ctx = 4
    ctx1 = execute(["tests.config.workflow_config_execute"])
    ctx2 = execute(["tests.config.workflow_config_execute"])
    assert ctx1.value == exp_value_ctx
    assert ctx1.value == exp_value_ctx

    # specifically check that ctx1.value and ctx2.value are different object
    ctx2.value += 1
    assert ctx1.value == exp_value_ctx

    # specifically check that ctx1.parameters.value and ctx2.parameters.value are different objects
    ctx1.parameters.value["value"] += 1
    assert ctx1.parameters.value["value"] == 5
    assert ctx2.parameters.value["value"] == 4


def test_execute_loop():

    ctxs = [None] * 3

    for i in range(len(ctxs)):
        ctxs[i] = execute(["tests.config.workflow_config_execute_loop"])

    exp_value_ctx = 64
    for i in range(len(ctxs)):
        assert ctxs[i].value == exp_value_ctx

    # specifically check that each context is a different object
    ctxs[0].value += 1
    for i in range(1, len(ctxs)):
        assert ctxs[i].value == exp_value_ctx

    # specifically check that ctx.parameters.value is a different objects
    ctxs[0].parameters.value["value"] += 1
    for i in range(1, len(ctxs)):
        assert ctxs[i].parameters.value["value"] == 4
