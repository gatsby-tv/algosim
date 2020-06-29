import colorama
from .cli import cli

def main():
    colorama.init()
    cli(auto_envvar_prefix="ALGOSIM")
