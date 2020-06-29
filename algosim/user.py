import logging

from numpy.random import randint
from colorama import Fore

from .model import Model


class User(Model):
    def __init__(self, faker, rng):
        super().__init__()
        self.rng = rng
        self.username = faker.user_name()
        self.ext = randint(10000, 99999)
        self.id = f"{self.username}#{self.ext}"

    def step(self, env, data, events):
        logging.debug(f"Starting process for user: {Fore.CYAN}{self.id}{Fore.WHITE}")
        while True:
            duration = self.rng()
            logging.debug(
                f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                f"is waiting for {Fore.YELLOW}{duration:.3f}{Fore.WHITE} units"
            )
            yield env.timeout(duration)
            selection = data.select(self.id, env.now)
            if selection:
                logging.debug(
                    f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                    f"decides to promote {selection} "
                    f"(rating -> {Fore.RED}{selection.rating(env.now)}{Fore.WHITE})"
                )
                events.submit(env.now, selection)
            else:
                logging.debug(
                    f"[{env.now:0>17.8f}] {Fore.CYAN}{self.id}{Fore.WHITE} "
                    "chooses not to promote a video"
                )
