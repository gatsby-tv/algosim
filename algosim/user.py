import logging

from numpy.random import randint
from colorama import Fore

from .model import Model
from .selection import FilterFunction, BiasFunction


class User(Model):
    def __init__(self, faker, wait_rng, selector, bias, filter):
        super().__init__()
        self.wait_rng = wait_rng
        self.username = faker.user_name()
        self.ext = randint(10000, 99999)
        self.id = f"{self.username}#{self.ext}"
        self.selector = selector
        self.bias = bias
        self.filter = filter
        self.promoted = []

    def step(self, env, data):
        logging.debug(f"Starting process for user: {Fore.CYAN}{self.id}{Fore.WHITE}")
        while True:
            duration = self.wait_rng()
            logging.debug(
                f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                f"is waiting for {Fore.YELLOW}{duration:.3f}{Fore.WHITE} units"
            )
            yield env.timeout(duration)

            selection = self.selector(env.now, self, data.videos)
            if selection:
                rating_before = selection.rating(env.now)
                selection.promote(env.now, self)
                self.promoted.append(selection)
                rating_after = selection.rating(env.now)
                data.update(env.now)

                logging.debug(
                    f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                    f"decides to promote {selection} "
                    f"(rating: {Fore.RED}{rating_before:.4f}{Fore.WHITE} "
                    f"-> {Fore.RED}{rating_after:.4f}{Fore.WHITE})"
                )
            else:
                logging.debug(
                    f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                    "chooses not to promote a video"
                )
