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

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({Fore.CYAN}{self.title}{Fore.WHITE}, "
            f"quality={Fore.MAGENTA}{self.quality:.4f}{Fore.WHITE})"
        )
