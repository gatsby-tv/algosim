import numpy as np

class Function(object):
    @classmethod
    def configure(cls, name, seed, config):
        rng = np.random.default_rng(seed)
        return type(name, (cls,), {"config": config if config else {}, "rng": rng})

    @classmethod
    def settings(cls, keys):
        return map(lambda k: float(cls.config[k]), keys)
