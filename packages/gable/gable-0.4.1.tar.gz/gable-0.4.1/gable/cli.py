import os
from typing import Optional

import click
from gable.client import GableClient

from .commands.auth import auth
from .commands.contract import contract
from .commands.data_asset import data_asset
from .commands.debug import debug
from .commands.ping import ping


class Context:
    def __init__(self):
        self.client: Optional[GableClient] = None


@click.group()
@click.option(
    "--endpoint",
    default=lambda: os.environ.get("GABLE_API_ENDPOINT", ""),
    help="Customer API endpoint for Gable, in the format https://api.company.gable.ai/",
)
@click.option(
    "--api-key",
    default=lambda: os.environ.get("GABLE_API_KEY", ""),
    help="API Key for Gable",
)
@click.version_option()
@click.pass_context
def cli(ctx, endpoint, api_key):
    ctx.obj = Context()
    ctx.obj.client = GableClient(endpoint, api_key)


cli.add_command(auth)
cli.add_command(debug)
cli.add_command(contract)
cli.add_command(data_asset)
cli.add_command(ping)


if __name__ == "__main__":
    cli()
