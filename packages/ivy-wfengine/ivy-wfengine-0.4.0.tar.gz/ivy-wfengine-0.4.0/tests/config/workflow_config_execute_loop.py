# Copyright (C) 2018 ETH Zurich, Institute for Particle Physics and Astrophysics

"""
Created on Oct 31, 2018
author: Joerg Herbel
"""

from ivy.loop import Loop
from ivy.utils.stop_criteria import RangeStopCriteria

plugins = [
    "tests.plugin.execute_plugin",
    Loop(
        ["tests.plugin.execute_plugin", "tests.plugin.execute_plugin"],
        stop=RangeStopCriteria(max_iter=2),
    ),
]

value = dict(value=2)
