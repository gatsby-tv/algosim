import logging

import numpy as np
import scipy.special as special

from .function import Function

class FilterFunction(Function):
    default = {"method": "no_repeat_promotions", "args": {}}

    @classmethod
    def none(cls, user, videos):
        return videos

    @classmethod
    def no_repeat_promotions(cls, user, videos):
        return [v for v in videos if v not in user.promoted]


class BiasFunction(Function):
    default = {"method": "quality", "args": {}}

    @classmethod
    def quality(cls, time, video):
        return video.quality

    @classmethod
    def quality_with_rating_saturation(cls, time, video):
        scale, alpha, offset = cls.settings(["scale", "alpha", "offset"])
        factor = scale / (1 + np.exp(alpha * (video.rating(time) - offset)))
        return factor * video.quality


class SelectorFunction(Function):
    @classmethod
    def maximum(cls, time, user, videos):
        videos = user.filter(user, videos)
        return max(videos, key=lambda v: user.bias(time, v))

    @classmethod
    def random(cls, time, user, videos):
        videos = user.filter(user, videos)
        return videos[int(cls.rng.uniform(0, len(videos)))]

    @classmethod
    def threshold(cls, time, user, videos):
        videos = user.filter(user, videos)
        value, = cls.settings(["value"])
        for video in videos:
            if user.bias(time, video) < threshold:
                return video

    @classmethod
    def fair_threshold(cls, time, user, videos):
        videos = videos.copy()
        cls.rng.shuffle(videos)
        return cls.threshold(time, user, videos)

    @classmethod
    def probability(cls, time, user, videos):
        videos = user.filter(user, videos)
        scale = cls.config.get("scale", 1)
        for video in videos:
            score = (special.erf(2 * scale * user.bias(time, video) - 1) + 1) / 2
            if cls.rng.uniform() < score:
                return video

    @classmethod
    def fair_probability(cls, time, user, videos):
        videos = videos.copy()
        cls.rng.shuffle(videos)
        return cls.probability(time, user, videos)
