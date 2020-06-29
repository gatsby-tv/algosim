from numpy.random import default_rng

class Rng(object):
    def __init__(self, seed, dist, **args):
        self.generator = getattr(default_rng(seed), dist) \
                if dist != "constant" else lambda **kwargs: kwargs["value"]
        self.args = args

    def __call__(self, **kwargs):
        return self.generator(**self.args, **kwargs)
