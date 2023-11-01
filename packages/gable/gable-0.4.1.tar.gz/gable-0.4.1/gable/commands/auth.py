import click
from click.core import Context as ClickContext


@click.group()
def auth():
    """View configured Gable authentication information"""


@auth.command()
@click.pass_context
def key(ctx: ClickContext):
    """Print the API Key gable is currently configured to use"""
    api_key = ctx.obj.client.api_key
    if api_key:
        click.echo("API Key in use: " + api_key)
        click.echo("To see your account's API Keys, visit your /settings page.")
    else:
        click.echo("No API Key configured.")
        click.echo("To see your account's API Keys, visit your /settings page.")
        click.echo(
            "Then you can use that key by setting the GABLE_API_KEY env var or using the --api-key flag."
        )
