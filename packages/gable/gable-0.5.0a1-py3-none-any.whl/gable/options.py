import functools
import os
import sys
from typing import Optional

import click
from gable.client import GableClient
from loguru import logger

gable_api_endpoint = None
gable_api_key = None


class Context:
    def __init__(self):
        self.client: Optional[GableClient] = None


def create_client_callback(ctx, param, value):
    if param.name == "endpoint":
        global gable_api_endpoint
        gable_api_endpoint = value
    elif param.name == "api_key":
        global gable_api_key
        gable_api_key = value
    if gable_api_endpoint and gable_api_key:
        if ctx.obj is None:
            ctx.obj = Context()
        # Once we've collected both values, create the client
        logger.debug(f"Creating Gable client with endpoint {gable_api_endpoint}")
        ctx.obj.client = GableClient(gable_api_endpoint, gable_api_key)
    return value


def endpoint_options(func):
    @click.option(
        "--endpoint",
        default=lambda: os.environ.get("GABLE_API_ENDPOINT", ""),
        # Don't pass these values to the subcommand functions
        expose_value=False,
        callback=create_client_callback,
        help="Customer API endpoint for Gable, in the format https://api.company.gable.ai/",
    )
    @click.option(
        "--api-key",
        default=lambda: os.environ.get("GABLE_API_KEY", ""),
        # Don't pass these values to the subcommand functions
        expose_value=False,
        callback=create_client_callback,
        help="API Key for Gable",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def configure_logger(ctx, param, value):
    if value:
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> - {message}",
        )
    return value


def global_options(func):
    @click.option(
        "--debug",
        is_flag=True,
        default=False,
        # Make eager so we can configure logging before the other options are parsed
        is_eager=True,
        # Don't pass these values to the subcommand functions
        expose_value=False,
        callback=configure_logger,
        help="Enable debug logging",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
