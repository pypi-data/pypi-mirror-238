# Copyright (C) 2018 ETH Zurich, Institute for Particle Physics and Astrophysics

"""
Created on Oct 31, 2018
author: Joerg Herbel
"""

from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.plugin.base_plugin import BasePlugin


class Plugin(BasePlugin):
    """
    Plugin that doubles ctx.value if present, else take value from parameters and double
    """

    def __str__(self):
        return __name__

    def __call__(self):
        if hasattr(self.ctx, "value"):
            self.ctx.value *= 2
        else:
            self.ctx.value = self.ctx.parameters.value["value"] * 2
            self.ctx.parameters.value["value"] += 2
