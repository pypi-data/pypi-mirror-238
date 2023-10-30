# Copyright (c) 2013 ETH Zurich, Institute for Astronomy

"""
Tests for `ivy.stop_criteria` module.
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from ivy import context
from ivy.utils.stop_criteria import RangeStopCriteria
from ivy.exceptions.exceptions import InvalidAttributeException
from ivy.loop import Loop


class TestStopCriteria(object):
    def test_range_stop_criteria(self):

        with pytest.raises(InvalidAttributeException):
            RangeStopCriteria(0)

        stop_criteria = RangeStopCriteria(1)
        loop = Loop("", ctx=context.create_ctx(), stop=stop_criteria)

        assert not stop_criteria.is_stop()

        context.loop_ctx(loop).increment()
        assert stop_criteria.is_stop()
