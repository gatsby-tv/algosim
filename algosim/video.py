from itertools import chain

import numpy as np
from colorama import Fore

from .rating import Promotion

class Video(object):
    def __init__(self, title, quality, rater):
        self.title = title
        self.quality = quality
        self.rater = rater
        self.promotions = []

    def promote(self, time, user, quantity=1):
        self.promotions.extend(quantity * [Promotion(time, user)])

    def rating(self, time):
        return self.rater(time, self.promotions)

    def history(self, time, steps=1000):
        def filter_promotions(time):
            return filter(lambda p: p.time < time, self.promotions)

        times = np.arange(0, time, time / steps)
        ratings = np.fromiter(map(lambda t: self.rater(t, filter_promotions(t)), times), float)
        return times, ratings

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({Fore.CYAN}{self.title}{Fore.WHITE}, "
            f"quality={Fore.MAGENTA}{self.quality:.4f}{Fore.WHITE})"
        )
