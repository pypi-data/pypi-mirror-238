# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.context` module.

author: jakeret
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from ivy.loop import Loop
from ivy.context import register
from ivy.exceptions.exceptions import InvalidLoopException
from ivy.context import loop_ctx
from ivy import context
from ivy.utils.struct import Struct
from ivy.utils.struct import ImmutableStruct


class TestContext(object):
    def test_register(self):

        ctx = context.create_ctx()
        loop = Loop("plugin", ctx=ctx)

        assert loop_ctx(loop) is not None

        with pytest.raises(InvalidLoopException):
            register(loop)

    def test_create_ctx(self):
        ctx = context.create_ctx()
        assert isinstance(ctx, Struct)

        ctx = context.create_ctx(a=3)
        assert isinstance(ctx, Struct)
        assert ctx.a == 3

        args = {"a": 3}
        ctx = context.create_ctx(**args)
        assert isinstance(ctx, Struct)
        assert ctx.a == 3

    def test_create_immu_ctx(self):
        ctx = context.create_immutable_ctx()
        assert isinstance(ctx, ImmutableStruct)

        ctx = context.create_immutable_ctx(a=3)
        assert isinstance(ctx, ImmutableStruct)
        assert ctx.a == 3

        args = {"a": 3}
        ctx = context.create_immutable_ctx(**args)
        assert isinstance(ctx, ImmutableStruct)
        assert ctx.a == 3
