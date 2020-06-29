from collections import namedtuple

import numpy as np


Promotion = namedtuple("Promotion", ["source", "time"])

class Rater(object):
    config = {}
    rng = None

    @staticmethod
    def configure(seed, settings):
        Rater.config = settings
        Rater.rng = np.random.default_rng(seed)

    @staticmethod
    def settings(keys):
        return map(lambda k: float(Rater.config[k]), keys)

    @staticmethod
    def logistic_decay(time, promotions):
        scale, alpha, offset = Rater.settings(["scale", "alpha", "offset"])
        return sum(map(
            lambda p: scale / (1 + np.exp(alpha*((time - p.time) - offset))),
            promotions
        ))
