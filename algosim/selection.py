import numpy as np
import scipy.special as special


class Selector(object):
    config = {}
    rng = None

    @staticmethod
    def configure(seed, settings):
        Selector.config = settings
        Selector.rng = np.random.default_rng(seed)

    @staticmethod
    def settings(keys):
        return map(lambda k: float(Selector.config[k]), keys)

    @staticmethod
    def highest_quality(time, videos):
        target = max([v.quality for v in videos])
        return next(filter(lambda v: v.quality == target, videos))

    @staticmethod
    def random(time, videos):
        videos[int(Selector.rng.uniform(0, len(videos)))]

    @staticmethod
    def quality_threshold(time, videos):
        threshold, = Selector.settings(["threshold"])
        for video in videos:
            if video.quality < threshold:
                return video

    @staticmethod
    def fair_quality_threshold(time, videos):
        videos = videos.copy()
        Selector.rng.shuffle(videos)
        return Selector.quality_threshold(time, videos)

    @staticmethod
    def quality_based_probability(time, videos):
        scale = Selector.config.get("scale", 1)
        for video in videos:
            if Selector.rng.uniform() < special.erf(scale * video.quality):
                return video

    @staticmethod
    def fair_quality_based_probability(time, videos):
        videos = videos.copy()
        Selector.rng.shuffle(videos)
        return Selector.quality_based_probability(time, videos)
