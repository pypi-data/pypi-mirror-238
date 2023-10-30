# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.context_provider` module.

author: jakeret
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os
from ivy.workflow_manager import WorkflowManager
from ivy.context_provider import PickleContextProvider
from ivy.context_provider import DefaultContextProvider
from ivy.utils.struct import Struct
from ivy.utils.struct import ImmutableStruct


class TestContextProvider(object):
    def test_create_ctx(self):
        ctx = DefaultContextProvider.create_context()
        assert isinstance(ctx, Struct)

        ctx = DefaultContextProvider.create_context(a=3)
        assert isinstance(ctx, Struct)
        assert ctx.a == 3

        args = {"a": 3}
        ctx = DefaultContextProvider.create_context(**args)
        assert isinstance(ctx, Struct)
        assert ctx.a == 3

    def test_create_immu_ctx(self):
        ctx = DefaultContextProvider.create_immutable_context()
        assert isinstance(ctx, ImmutableStruct)

        ctx = DefaultContextProvider.create_immutable_context(a=3)
        assert isinstance(ctx, ImmutableStruct)
        assert ctx.a == 3

        args = {"a": 3}
        ctx = DefaultContextProvider.create_immutable_context(**args)
        assert isinstance(ctx, ImmutableStruct)
        assert ctx.a == 3


class TestPickleContextProvider(object):
    def test_cust_ctx_provider(self):

        args = ["tests.config.workflow_config_cust"]

        mgr = WorkflowManager(args)
        mgr.launch()

        from ivy.context import get_context_provider

        assert get_context_provider() == PickleContextProvider

    def test_store_context(self, tmpdir):

        path = str(tmpdir.join("le_ctx"))
        ctx = DefaultContextProvider.create_context()
        ctx.ctx_file_name = path
        PickleContextProvider.store_context(ctx)
        assert os.path.exists(path)
        os.remove(path)
