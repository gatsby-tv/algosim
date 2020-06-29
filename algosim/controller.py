import logging

from simpy import Environment
from faker import Faker

from .selection import Selector
from .rating import Rater
from .rng import Rng
from .user import User
from .data import Database
from .events import Events


class Controller(object):
    def __init__(self, config):
        self.env = Environment()
        self.duration = config["duration"]
        seed = config.get("seed")
        faker = Faker()
        faker.seed_instance(seed)
        user_rng = Controller._get_rng(seed, config, ["users", "wait_time_distribution"])
        quality_rng = Controller._get_rng(seed, config, ["videos", "quality_distribution"])
        rater = Controller._get_method(config, ["rating", "method"])
        selector = Controller._get_method(config, ["selection", "method"])
        Rater.configure(seed, config["rating"]["args"])
        Selector.configure(seed, config["selection"]["args"])

        self.data = Database(
            config["videos"]["count"],
            faker,
            rater,
            selector,
            quality_rng,
            keep_sorted = config["videos"].get("keep_sorted", True)
        )
        self.events = Events()

        for _ in range(config["users"]["count"]):
            User(faker, user_rng).process(self.env, self.data, self.events)

    @staticmethod
    def _get_rng(seed, config, keys):
        settings = config
        for key in keys:
            settings = settings[key]
        method = settings["method"]
        args = settings["args"]
        return Rng(seed, method.lower().replace(" ", "_"), **args)

    @staticmethod
    def _get_method(config, keys):
        setting = config
        for key in keys:
            setting = setting[key]
        return setting.lower().replace(" ", "_")

    @classmethod
    def from_toml(cls, config):
        from toml import load
        return cls(load(config))

    def run(self):
        logging.info("Starting simulation...")
        self.env.run(until=self.duration)
        logging.info("Simulation completed.")
