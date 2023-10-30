__author__ = "Joel Akeret"
__email__ = "jakeret@phys.ethz.ch"
__version__ = "0.3.1"
__credits__ = "ETH Zurich, Institute for Astronomy"


import copyreg as copyreg

import types


# register custom reduce method for type MethodType
def reduce_method(m):
    return getattr, (m.__self__, m.__func__.__name__)


copyreg.pickle(types.MethodType, reduce_method)


from ivy import context
from ivy.workflow_manager import WorkflowManager
from ivy.workflow_manager import load_configs


def execute(args, **kwargs):
    """
    Runs a workflow for the given arguments.
    :param args: list of arguments which should be passed to ivy. The last argument has to be the config. Can also be a
                 single config string only.
    :param kwargs: keyword arguments that overwrite values in the config and in args
    :returns: the context of the workflow
    """
    mgr = WorkflowManager(args, **kwargs)
    mgr.launch()
    return mgr.ctx
