import click
from gable.client import GableClient
from gable.helpers.jsonpickle import register_jsonpickle_handlers
from gable.options import Context, endpoint_options, global_options
from loguru import logger

from .commands.auth import auth
from .commands.contract import contract
from .commands.data_asset import data_asset
from .commands.debug import debug
from .commands.ping import ping

# Configure logging to be off by default - note that click.echo() will still work
logger.remove()
# Configure jsonpickle's custom serialization handlers
register_jsonpickle_handlers()


@click.group()
@click.version_option()
@global_options
@endpoint_options
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = Context()
    if ctx.obj.client is None:
        # Create a client without an endpoint or api key by default, this will either be overwritten when the
        # endpoint/api options are processed, or the client validation will fail when the client is used
        ctx.obj.client = GableClient("", "")


cli.add_command(auth)
cli.add_command(debug)
cli.add_command(contract)
cli.add_command(data_asset)
cli.add_command(ping)


if __name__ == "__main__":
    cli()
