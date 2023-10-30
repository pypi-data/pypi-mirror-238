# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.cli` module.
author: jakeret
"""

from ivy.cli.main import _main


class TestCli(object):
    def test_launch_loop(self):
        ctx = _main(*["tests.config.workflow_config_cli"])
        assert ctx is not None
        assert ctx.params is not None
        assert ctx.params.plugins is not None
        assert len(ctx.timings) == 2
