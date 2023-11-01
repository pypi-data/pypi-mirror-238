import logging
import os
from importlib.metadata import version

import click

from .util import random_list, save_all_lists, save_specific_list

logger = logging.getLogger(__name__)
env = os.environ.get("DEPLOYMENT_ENV", "prod")
log_level = logging.INFO
if env != "prod":
    log_level = logging.DEBUG
logging.basicConfig(level=log_level)


def print_version(ctx, param, value):
    # print(ctx.__dict__)
    # print(param.__dict__)
    # print(value)
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'Version: {version("spotify-playlist")}')
    ctx.exit()


@click.group()
@click.option(
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Package version.",
)
def cli():
    pass


@cli.command()
@click.option(
    "--client-id", "-i",
    default="890f2ab03b8e4a94a33f66c9e83272ae",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="939cdd453c59404eacd2ff9682820920",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
@click.option(
    "--output-folder", "-o",
    default=os.getcwd(),
    show_default=True,
    type=click.Path(exists=True),
    required=False,
    help="output path.",
)
def all(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    os.chdir(kwargs.get("output_folder"))
    save_all_lists(env)


@cli.command()
@click.option(
    "--client-id", "-i",
    default="890f2ab03b8e4a94a33f66c9e83272ae",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="939cdd453c59404eacd2ff9682820920",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
@click.option(
    "--output-folder", "-o",
    default=os.getcwd(),
    show_default=True,
    type=click.Path(exists=True),
    required=False,
    help="output path.",
)
@click.argument('playlist', nargs=-1)
def name(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    os.chdir(kwargs.get("output_folder"))
    save_specific_list(env, kwargs.get("playlist"))


@cli.command()
@click.option(
    "--client-id", "-i",
    default="890f2ab03b8e4a94a33f66c9e83272ae",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="939cdd453c59404eacd2ff9682820920",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
def rand(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    random_list(env)


if __name__ == "__main__":
    cli()
