from pathlib import Path
import logging

import click

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
def cli(verbose, config):
    set_verbosity(verbose)
    config = Path(config)
    if not config.exists():
        logging.error(f"File `{config}` could not be found")
        exit(1)
    controller = Controller.from_toml(config)
    results = controller.run()
