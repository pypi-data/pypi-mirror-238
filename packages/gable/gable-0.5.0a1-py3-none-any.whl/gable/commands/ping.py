import click
from click.core import Context as ClickContext


@click.command()
@click.pass_context
def ping(ctx: ClickContext):
    """Pings the Gable API to check for connectivity"""
    try:
        response, success, status_code = ctx.obj.client.get("v0/ping")
    except Exception as e:
        raise click.ClickException(
            f"Unable to ping Gable API at {ctx.obj.client.endpoint}: {str(e)}"
        )
    if not success:
        raise click.ClickException(
            f"Unable to ping Gable API at {ctx.obj.client.endpoint}"
        )
    click.echo(f"Successfully pinged Gable API at {ctx.obj.client.endpoint}")
