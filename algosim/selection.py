import numpy as np
import scipy.special as special


class Bias(object):
    config = {}
    default = {"method": "quality", "args": {}}
    rng = None

    @staticmethod
    def configure(seed, settings):
        Bias.config = settings
        Bias.rng = np.random.default_rng(seed)

    @staticmethod
    def quality(time, video):
        return video.quality


class Selector(object):
    config = {}
    rng = None
    bias = None

    @staticmethod
    def configure(seed, settings):
        bias = settings.pop("bias", Bias.default)
        Bias.configure(seed, bias["args"])
        Selector.bias = getattr(Bias, bias["method"].lower().replace(" ", "_"))
        Selector.config = settings
        Selector.rng = np.random.default_rng(seed)

    @staticmethod
    def settings(keys):
        return map(lambda k: float(Selector.config[k]), keys)

    @staticmethod
    def maximum(time, videos):
        # TODO: fix so that we can use this method for biases with rng.
        target = max([Selector.bias(time, v) for v in videos])
        return next(filter(lambda v: Selector.bias(time, v) == target, videos))

    @staticmethod
    def random(time, videos):
        videos[int(Selector.rng.uniform(0, len(videos)))]

    @staticmethod
    def threshold(time, videos):
        threshold, = Selector.settings(["threshold"])
        for video in videos:
            if Selector.bias(time, video) < threshold:
                return video

    @staticmethod
    def fair_threshold(time, videos):
        videos = videos.copy()
        Selector.rng.shuffle(videos)
        return Selector.threshold(time, videos)

    @staticmethod
    def probability(time, videos):
        scale = Selector.config.get("scale", 1)
        for video in videos:
            if Selector.rng.uniform() < special.erf(scale * Selector.bias(time, video)):
                return video

    @staticmethod
    def fair_probability(time, videos):
        videos = videos.copy()
        Selector.rng.shuffle(videos)
        return Selector.probability(time, videos)
