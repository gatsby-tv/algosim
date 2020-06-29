from collections import namedtuple

import numpy as np

from .function import Function

Promotion = namedtuple("Promotion", ["time", "user"])

class RaterFunction(Function):
    @classmethod
    def logistic_decay(cls, time, promotions):
        scale, alpha, offset = cls.settings(["scale", "alpha", "offset"])
        return sum(map(
            lambda p: scale / (1 + np.exp(alpha*((time - p.time) - offset))),
            promotions
        ))
