import logging

from simpy import Environment
from faker import Faker

from .selection import SelectorFunction, BiasFunction, FilterFunction
from .rating import RaterFunction
from .rng import Rng
from .user import User
from .data import Database
from .events import Events


class Controller(object):
    def __init__(self, config):
        self.env = Environment()
        self.duration = config["duration"]
        seed = config.get("seed")
        if seed is not None:
            seed = abs(hash(seed))
        faker = Faker()
        faker.seed_instance(seed)
        user_rng = Controller._get_rng(seed, config, ["wait_time_distribution"])
        quality_rng = Controller._get_rng(seed, config, ["videos", "quality_distribution"])

        Rater = RaterFunction.configure("Rater", seed, config["rating"].get("args"))
        rater_method = Controller._get_method(config, ["rating", "method"])
        rater = getattr(Rater, rater_method)

        self.data = Database(
            config["videos"]["count"],
            faker,
            rater,
            quality_rng,
            keep_sorted = config["videos"].get("keep_sorted", True)
        )
        self.events = Events()

        for user in config["users"]:
            selection_conf = user["selection"]
            bias_conf = user.get("bias")
            filter_conf = user.get("filter")

            if not bias_conf:
                bias_conf = BiasFunction.default
            if not filter_conf:
                filter_conf = FilterFunction.default

            Selector = SelectorFunction.configure("Selector", seed, selection_conf.get("args"))
            Bias = BiasFunction.configure("Bias", seed, bias_conf.get("args"))
            Filter = FilterFunction.configure("Filter", seed, filter_conf.get("args"))
            selector = getattr(Selector, Controller._get_method(selection_conf, ["method"]))
            bias = getattr(Bias, Controller._get_method(bias_conf, ["method"]))
            filter = getattr(Filter, Controller._get_method(filter_conf, ["method"]))

            for _ in range(user["count"]):
                User(faker, user_rng, selector, bias, filter).process(self.env, self.data, self.events)

    @staticmethod
    def _get_rng(seed, config, keys):
        settings = config
        for key in keys:
            settings = settings[key]
        method = settings["method"]
        args = settings.get("args", {})
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
