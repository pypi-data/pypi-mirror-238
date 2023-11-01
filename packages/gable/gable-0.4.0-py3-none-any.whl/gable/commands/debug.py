import os
import pprint

import click
from click.core import Context as ClickContext


@click.group(hidden=True)
def debug():
    """Debug commands for the cli"""


@debug.command()
@click.argument(
    "path", type=click.Path(exists=True, file_okay=False), default=os.getcwd()
)
def git_info(path: os.PathLike):
    """Prints the git information for the given directory"""
    from gable.helpers.repo_interactions import get_git_repo_info

    pprint.pprint(get_git_repo_info(path))


@debug.command()
@click.pass_context
def env(_ctx: ClickContext):
    """Prints the environment variables used to configure Gable"""
    env_vars = ["GABLE_API_ENDPOINT", "GABLE_API_KEY"]
    for env_var in env_vars:
        click.echo(f"{env_var}={os.environ.get(env_var, '<Not Set>')}")
    click.echo(
        "Note: these can be overridden by passing command line arguments to gable."
    )
