# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 4, 2014
author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
from ivy.context import loop_ctx
from ivy.utils.struct import WorkflowState
from ivy.exceptions.exceptions import InvalidAttributeException


class StopCriteria(object):
    """
    Abstract implementation of stopping criteria
    """

    __metaclass__ = ABCMeta

    parent = None

    @abstractmethod
    def is_stop(self):
        pass


class RangeStopCriteria(StopCriteria):
    """
    Stopping criteria which stops after `maxIter` iterations
    """

    def __init__(self, max_iter):
        if max_iter < 1:
            raise InvalidAttributeException("Minimum iteration is 1")

        self.maxIter = max_iter

    def is_stop(self):

        ctx = loop_ctx(self.parent)

        if ctx.iter >= self.maxIter:
            ctx.stop()

        return ctx.state == WorkflowState.STOP


class SimpleStopCriteria(RangeStopCriteria):
    """
    Simple implementation of a stopping criteria. Stops after `one` iteration
    """

    def __init__(self):
        super(SimpleStopCriteria, self).__init__(max_iter=1)
