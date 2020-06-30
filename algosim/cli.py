from pathlib import Path
import logging

import click
import numpy as np
import matplotlib.pyplot as plt

from .controller import Controller


def set_verbosity(v):
    level = logging.DEBUG if v is 2 else logging.INFO if v is 1 else logging.WARNING
    logging.basicConfig(
        level=level,
        format="(%(levelname)s) %(message)s",
    )

@click.command()
@click.option("-v", "--verbose", count=True)
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False, exists=False, readable=True),
    default="./config.toml",
    show_default=True,
)
@click.option(
    "-p",
    "--plot",
)
def cli(verbose, config, plot):
    set_verbosity(verbose)
    config = Path(config)
    if not config.exists():
        logging.error(f"File `{config}` could not be found")
        exit(1)
    controller = Controller.from_toml(config)
    results = controller.run()
    if plot is not None:
        keywords = set(plot.lower().split(" "))

        def search(data):
            test = data.video.title.lower().replace("!?", "").split(" ")
            return all([key in test for key in keywords])

        targets = list(filter(search, results))

        if targets:
            plt.plot(targets[0].times, targets[0].ratings)
            plt.show()
