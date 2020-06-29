from numpy.linalg import norm
from faker import Faker

from .video import Video

class Database(object):
    def __init__(self, count, faker, rater, quality_rng, keep_sorted=True):
        self.keep_sorted = keep_sorted
        qualities = quality_rng(size=count)
        self.videos = []
        for quality in qualities:
            # We replace periods with "!?" to make the data look more realistic.
            title = faker.text(60).replace(".", "!?")
            self.videos.append(Video(title, quality, rater))

    def update(self, time):
        if self.keep_sorted:
            self.videos.sort(key=lambda v: v.rating(time), reverse=True)

    def select(self, time, user, quantity=1):
        selection = user.selector(time, user, self.videos)
        if selection is None:
            return
        selection.promote(time, user, quantity)
        if self.keep_sorted:
            self.videos.sort(key=lambda v: v.rating(time), reverse=True)
        return selection
