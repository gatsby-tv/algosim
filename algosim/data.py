from numpy.linalg import norm
from faker import Faker

from .selection import Selector
from .video import Video

class Database(object):
    def __init__(self, count, faker, rater, selector, quality_rng, keep_sorted=True):
        self.keep_sorted = keep_sorted
        self.selector = getattr(Selector, selector)
        qualities = quality_rng(size=count)
        self.videos = []
        for quality in qualities:
            # We replace periods with "!?" to make the data look more realistic.
            title = faker.text(60).replace(".", "!?")
            self.videos.append(Video(title, quality, rater))

    def select(self, source, time, quantity=1):
        selection = self.selector(time, self.videos)
        if selection is None:
            return
        selection.promote(source, time, quantity)
        if self.keep_sorted:
            self.videos.sort(key=lambda v: v.rating(time), reverse=True)
        return selection
