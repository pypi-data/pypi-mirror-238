# Copyright 2013 ETHZ.ch Lukas Gamper <lukas.gamper@usystems.ch>

from ivy.exceptions.exceptions import InvalidLoopException
from ivy.utils.struct import WorkflowStruct


def register(loop):
    try:
        loop_ctx(loop)
        raise InvalidLoopException()
    except (KeyError, AttributeError):
        loop.ctx[loop] = WorkflowStruct()


def loop_ctx(loop):
    return loop.ctx[loop]


def create_ctx(**args):
    return get_context_provider().create_context(**args)


def create_immutable_ctx(**args):
    return get_context_provider().create_immutable_context(**args)


def get_context_provider():
    from ivy.context_provider import DefaultContextProvider

    return DefaultContextProvider
