# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Mar 6, 2014

author: jakeret
"""

from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
import pickle
from ivy.utils.struct import ImmutableStruct


class DefaultContextProvider(object):
    """
    Default implementation of a context provider.
    Creates a simple mutable struct as ctx and doesn't
    persist the context.
    """

    @staticmethod
    def create_context(**args):
        """
        Returns a Struct
        """
        return Struct(**args)

    @staticmethod
    def create_immutable_context(**args):
        """
        Returns a Struct
        """
        return ImmutableStruct(**args)

    @staticmethod
    def store_context(ctx):
        """
        Dummy method. Nothing is stored
        """
        pass


class PickleContextProvider(DefaultContextProvider):
    """
    Extends the DefaultContextProvider.
    Persists the context to the disk by using pickle.
    Requires the attribute 'ctx_file_name' in the ctx
    """

    @staticmethod
    def store_context(ctx):
        """
        Writes the current ctx to the disk
        """
        filename = ctx.ctx_file_name
        with open(filename, "wb") as ctxFile:
            pickle.dump(ctx, ctxFile)
