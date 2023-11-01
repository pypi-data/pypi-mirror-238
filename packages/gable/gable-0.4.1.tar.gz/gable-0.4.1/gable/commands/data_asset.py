import json
from typing import cast

import click
from click.core import Context as ClickContext
from click_option_group import AllOptionGroup, optgroup
from gable.helpers.check import (
    post_data_asset_check_requests,
    post_data_assets_check_requests,
)
from gable.helpers.data_asset import (
    get_db_connection,
    get_db_schema_contents,
    get_schema_contents,
    get_source_names,
    send_schemas_to_gable,
    standardize_source_type,
    validate_db_input_args,
)
from gable.helpers.emoji import EMOJI
from gable.helpers.multi_option import MultiOption
from gable.helpers.repo_interactions import get_git_repo_info, get_git_ssh_file_path
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetNoContractResponse,
    ErrorResponse,
    ResponseType,
)
from gable.readers.file import read_file
from rich.console import Console
from rich.table import Table

console = Console()


@click.group(name="data-asset")
def data_asset():
    """Commands for data assets"""


@data_asset.command(name="list")
@click.pass_context
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Format of the output. Options are: table (default) or json",
)
@click.option(
    "--full",
    is_flag=True,
    help="Return full data asset details including namespace and name",
)
def list_data_assets(ctx: ClickContext, output: str, full: bool) -> None:
    """List all data assets"""
    # Get the data
    response, success, status_code = ctx.obj.client.get("v0/data-assets")

    # Format the output
    if output == "json":
        data_asset_list = []
        for data_asset in response:
            row = {"resourceName": f"{data_asset['namespace']}:{data_asset['name']}"}
            if full:
                # Filter out invalid data assets...
                if "://" in data_asset["namespace"]:
                    row["type"] = data_asset["namespace"].split("://", 1)[0]
                    row["dataSource"] = data_asset["namespace"].split("://", 1)[1]
                    row["name"] = data_asset["name"]
            data_asset_list.append(row)
        click.echo(json.dumps(data_asset_list))
    else:
        table = Table(show_header=True, title="Data Assets")
        table.add_column("resourceName")
        if full:
            table.add_column("type")
            table.add_column("dataSource")
            table.add_column("name")
        for data_asset in response:
            if not full:
                table.add_row(f"{data_asset['namespace']}:{data_asset['name']}")
            else:
                # Filter out invalid data assets...
                if "://" in data_asset["namespace"]:
                    table.add_row(
                        f"{data_asset['namespace']}:{data_asset['name']}",
                        data_asset["namespace"].split("://", 1)[0],
                        data_asset["namespace"].split("://", 1)[1],
                        data_asset["name"],
                    )
        console.print(table)


@data_asset.command(
    name="register",
    epilog="""Example:

gable data-asset register --source-type postgres --host prod.pg.db.host --db transit --schema public --table routes""",
)
@click.pass_context
@click.option(
    "--source-type",
    required=True,
    type=click.Choice(
        ["postgres", "mysql", "avro", "protobuf", "json_schema"], case_sensitive=True
    ),
    help="""The type of data asset.
    
    For databases (postgres, mysql) a data asset is a table within the database.

    For protobuf/avro/json_schema a data asset is message/record/schema within a file.
    """,
)
@optgroup.group(
    "Database Options",
    help="""Options for registering database tables as data assets. Gable relies on having a proxy database that mirrors your 
    production database, and will connect to the proxy database to register tables as data assets. This is to ensure that 
    Gable does not have access to your production data, or impact the performance of your production database in any way. 
    The proxy database can be a local Docker container, a Docker container that is spun up in your CI/CD workflow, or a
    database instance in a test/staging environment. The tables in the proxy database must have the same schema as your 
    production database for all tables to be correctly registered. The proxy database must be accessible from the 
    machine that you are running the gable CLI from.

    If you're registering tables in your CI/CD workflow, it's important to only register from the main branch, otherwise 
    you may end up registering tables that do not end up in production.
    """,
)
@optgroup.option(
    "--host",
    "-h",
    type=str,
    help="""The host name of the production database, for example 'service-one.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com'.
    Despite not needing to connect to the production database, the host is still needed to generate the unique resource 
    name for the data asset. For example, a Postgres resource name is 'postgres://<host>:<port>:<db>.<schema>.<table>'
    """,
)
@optgroup.option(
    "--port",
    "-p",
    type=int,
    help="""The port of the production database. Despite not needing to connect to the production database, the port 
    is still needed to generate the unique resource name for the data asset. For example, a Postgres resource name is 
    'postgres://<host>:<port>:<db>.<schema>.<table>'""",
)
@optgroup.option(
    "--db",
    type=str,
    help="""The name of the production database. Despite not needing to connect to 
    the production database, the database name is still needed to generate the unique resource name for the data 
    asset. For example, a Postgres resource name is 'postgres://<host>:<port>:<db>.<schema>.<table>'
    
    Database naming convention frequently includes the environment (production/development/test/staging) in the 
    database name, so this value may not match the name of the database in the proxy database instance. If this is 
    the case, you can set the --proxy-db value to the name of the database in the proxy instance, but we'll use the 
    value of --db to generate the unique resource name for the data asset.
    
    For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
    you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.""",
)
@optgroup.option(
    "--schema",
    "-s",
    type=str,
    help="""The schema of the production database where the table(s) you want to register are located. Despite not 
    needing to connect to the production database, the schema name is still needed to generate the unique resource 
    name for the data asset. For example, a Postgres resource name is 'postgres://<host>:<port>:<db>.<schema>.<table>'
    
    Database naming convention frequently includes the environment (production/development/test/staging) in the 
    schema name, so this value may not match the name of the schema in the proxy database instance. If this is 
    the case, you can set the --proxy-schema value to the name of the schema in the proxy instance, but we'll use the 
    value of --schema to generate the unique resource name for the data asset.
    
    For example, if your production schema is 'production', but your test database is 'test', 
    you would set --schema to 'production' and --proxy-schema to 'test'.""",
)
@optgroup.option(
    "--table",
    "-t",
    type=str,
    default=None,
    help="""The table to register as a data asset. If no table is specified, all tables within the provided schema will be registered.

    Table names in the proxy database instance must match the table names in the production database instance, even if
    the database or schema names are different.""",
)
@optgroup.option(
    "--proxy-host",
    "-ph",
    type=str,
    help="""The host string of the database instance that serves as the proxy for the production database. This is the 
    database that Gable will connect to when registering tables as data assets instead of connecting to your production database. 
    For example: in your CI/CD workflow you can start a local Docker container, apply the same migrations as your production 
    database, and pass 'localhost' as the proxy host value.
    """,
)
@optgroup.option(
    "--proxy-port",
    "-pp",
    type=int,
    help="""The port of the database instance that serves as the proxy for the production database. This is the 
    database that Gable will connect to when registering tables as data assets instead of connecting to your production database. 
    For example: in your CI/CD workflow you can start a local Docker container, apply the same migrations as your production 
    database, and pass the port you exposed on the Docker container as the proxy host value.
    """,
)
@optgroup.option(
    "--proxy-db",
    "-pdb",
    type=str,
    default=None,
    help="""Only needed if the name of the database in the proxy instance is different than the name of the
    production database.

    If not specified, the value of --db will be used to generate the unique resource name for the data asset. For example, if
    your production database is 'prod_service_one', but your test database is 'test_service_one', you would set --db to
    'prod_service_one' and --proxy-db to 'test_service_one'.
    """,
)
@optgroup.option(
    "--proxy-schema",
    "-ps",
    type=str,
    default=None,
    help="""Only needed if the name of the schema in the proxy instance is different than the name of the schema in the
    production database.

    If not specified, the value of --schema will be used to generate the unique resource name for the data asset. For example, if
    your production schema is 'production', but your test database is 'test', you would set --schema to
    'production' and --proxy-schema to 'test'.
    """,
)
@optgroup.option(
    "--proxy-user",
    "-pu",
    type=str,
    help="""The user that will be used to connect to the database instance that serves as the proxy for the production database. 
    This is the database that Gable will connect to when registering tables as data assets instead of connecting to your 
    production database. For example: in your CI/CD workflow you can start a local Docker container, apply the same migrations 
    as your production database, and pass  the default user for the database ('postgres' for PostgresQL, 'root' for MySQL) as 
    the proxy username password.
    """,
)
@optgroup.option(
    "--proxy-password",
    "-ppw",
    type=str,
    help="""If specified, the password that will be used to connect to the database instance that serves as the proxy for 
    the production database. This is the database that Gable will connect to when registering tables as data assets instead 
    of connecting to your production database. For example: in your CI/CD workflow you can start a local Docker container, 
    apply the same migrations as your production database, and pass  the default user for the database ('postgres' for 
    PostgresQL) as the proxy username password, or leave it blank if the default credentials don't have a password.
    """,
)
@optgroup.group(
    "Protobuf & Avro options",
    help="""Options for registering a Protobuf message, Avro record, or JSON schema object as data assets. These objects 
    represent data your production services produce, regardless of the transport mechanism. 

    If you're registering Protobuf messages, Avro records, or JSON schema objects in your CI/CD workflow, it's important 
    to only register from the main branch, otherwise you may end up registering records that do not end up in production.
    """,
    cls=AllOptionGroup,
)
@optgroup.option("--files", type=tuple, cls=MultiOption)
def register_data_asset(
    ctx: ClickContext,
    source_type: str,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: str,
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
) -> None:
    """Registers a data with Gable"""
    # Standardize the source type
    source_type = standardize_source_type(source_type)
    if source_type in ["postgres", "mysql"]:
        proxy_db = proxy_db if proxy_db else db
        proxy_schema = proxy_schema if proxy_schema else schema
        files_list: list[str] = []
    else:
        # Turn the files tuple into a list
        files_list: list[str] = list(files)
    # This won't be set for file-based data assets, but we need to pass through
    # the real db.schema value in case the proxy database has different names
    database_schema = ""

    source_names: list[str] = []
    schema_contents: list[str] = []
    # Validate the source type arguments and get schema contents
    if source_type in ["postgres", "mysql"]:
        validate_db_input_args(proxy_user, proxy_password, proxy_db)
        connection = get_db_connection(
            source_type, proxy_user, proxy_password, proxy_db, proxy_host, proxy_port
        )
        schema_contents.append(
            json.dumps(get_db_schema_contents(connection, proxy_schema, table=table))
        )

        database_schema = f"{db}.{schema}"
        source_names.append(f"{host}:{port}")
    elif source_type in ["avro", "protobuf", "json_schema"]:
        for file in files_list:
            schema_contents.append(read_file(file))
            source_names.append(get_git_ssh_file_path(get_git_repo_info(file), file))
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")
    # Send the schemas to Gable
    response, success, status_code = send_schemas_to_gable(
        ctx.obj.client, source_type, source_names, database_schema, schema_contents
    )
    if not success:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Registration failed for some data assets: {str(response)}"
        )
    click.echo(
        f"{EMOJI.GREEN_CHECK.value} Registration successful: {response['registered']}"
    )


@data_asset.command(
    name="check",
    epilog="""Example:

gable data-asset check --source-type protobuf --files ./**/*.proto""",
)
@click.pass_context
@click.option(
    "--source-type",
    required=True,
    type=click.Choice(
        ["postgres", "mysql", "avro", "protobuf", "json_schema"], case_sensitive=True
    ),
    help="""The type of data asset.
    
    For databases (postgres, mysql) the check will be performed for all tables within the database.

    For protobuf/avro/json_schema the check will be performed for all file(s)
    """,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Format of the output. Options are: text (default), json, or markdown which is intended to be used as a PR comment",
)
@optgroup.group(
    "Database Options",
    help="""Options for checking contract complaince for tables in a relational database. The check will be performed
    for any tables that have a contract associated with them.
    
    Gable relies on having a proxy database that mirrors your production database, and will connect to the proxy database
    to perform the check in order to perform the check as part of the CI/CD process before potential changes in the PR are
    merged.
    """,
)
@optgroup.option(
    "--host",
    "-h",
    type=str,
    help="""The host name of the production database, for example 'service-one.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com'.
    Despite not needing to connect to the production database, the host is still needed to generate the unique resource 
    name for the real data asset so we can look up any associated contracts.
    """,
)
@optgroup.option(
    "--port",
    "-p",
    type=int,
    help="""The port of the production database. Despite not needing to connect to the production database, the port is 
    still needed to generate the unique resource name for the real data asset so we can look up any associated contracts.
    """,
)
@optgroup.option(
    "--db",
    type=str,
    help="""The name of the production database. Despite not needing to connect to the production database, the database 
    name is still needed to generate the unique resource name for the real data asset so we can look up any associated 
    contracts.
    
    Database naming convention frequently includes the environment (production/development/test/staging) in the 
    database name, so this value may not match the name of the database in the proxy database instance. If this is 
    the case, you can set the --proxy-db value to the name of the database in the proxy instance, but we'll use the 
    value of --db to generate the unique resource name for the data asset.
    
    For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
    you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.""",
)
@optgroup.option(
    "--schema",
    "-s",
    type=str,
    help="""The schema of the production database where the table(s) you want to register are located. Despite not 
    needing to connect to the production database, the schema is still needed to generate the unique resource name 
    for the real data asset so we can look up any associated contracts.'
    
    Database naming convention frequently includes the environment (production/development/test/staging) in the 
    schema name, so this value may not match the name of the schema in the proxy database instance. If this is 
    the case, you can set the --proxy-schema value to the name of the schema in the proxy instance, but we'll use the 
    value of --schema to generate the unique resource name for the data asset.
    
    For example, if your production schema is 'production', but your test database is 'test', 
    you would set --schema to 'production' and --proxy-schema to 'test'.""",
)
@optgroup.option(
    "--table",
    "-t",
    type=str,
    default=None,
    help="""The table to check for contract violations. If no table is specified, all tables within the provided 
    schema will be checked.

    Table names in the proxy database instance must match the table names in the production database instance, even if
    the database or schema names are different.""",
)
@optgroup.option(
    "--proxy-host",
    "-ph",
    type=str,
    help="""The host string of the database instance that serves as the proxy for the production database. This is the 
    database that Gable will connect to when checking tables for contract violations in the CI/CD workflow.
    """,
)
@optgroup.option(
    "--proxy-port",
    "-pp",
    type=int,
    help="""The port of the database instance that serves as the proxy for the production database. This is the 
    database that Gable will connect to when checking tables for contract violations in the CI/CD workflow.
    """,
)
@optgroup.option(
    "--proxy-db",
    "-pdb",
    type=str,
    default=None,
    help="""Only needed if the name of the database in the proxy instance is different than the name of the
    production database.

    If not specified, the value of --db will be used to generate the unique resource name for the data asset. For example, if
    your production database is 'prod_service_one', but your test database is 'test_service_one', you would set --db to
    'prod_service_one' and --proxy-db to 'test_service_one'.
    """,
)
@optgroup.option(
    "--proxy-schema",
    "-ps",
    type=str,
    default=None,
    help="""Only needed if the name of the schema in the proxy instance is different than the name of the schema in the
    production database.

    If not specified, the value of --schema will be used to generate the unique resource name for the data asset. For example, if
    your production schema is 'production', but your test database is 'test', you would set --schema to
    'production' and --proxy-schema to 'test'.
    """,
)
@optgroup.option(
    "--proxy-user",
    "-pu",
    type=str,
    help="""The user that will be used to connect to the proxy database instance that serves as the proxy for the production 
    database. This is the database that Gable will connect to when checking tables for contract violations in the CI/CD workflow. 
    """,
)
@optgroup.option(
    "--proxy-password",
    "-ppw",
    type=str,
    default=None,
    help="""If specified, the password that will be used to connect to the proxy database instance that serves as the proxy for 
    the production database. This is the database that Gable will connect to when checking tables for contract violations in 
    the CI/CD workflow. 
    """,
)
@optgroup.group(
    "Protobuf & Avro options",
    help="""Options for checking Protobuf message(s), Avro record(s), or JSON schema object(s)for contract violations.""",
    cls=AllOptionGroup,
)
@optgroup.option("--files", type=tuple, cls=MultiOption)
def check_data_asset(
    ctx: ClickContext,
    source_type: str,
    output: str,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: str,
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
) -> None:
    """Checks data asset(s) against a contract"""
    # Standardize the source type
    source_type = standardize_source_type(source_type)
    if source_type in ["postgres", "mysql"]:
        files_list: list[str] = []
    else:
        # Turn the files tuple into a list
        files_list: list[str] = list(files)
    schema_contents = get_schema_contents(
        source_type=source_type,
        dbuser=proxy_user,
        dbpassword=proxy_password,
        db=proxy_db,
        dbhost=proxy_host,
        dbport=proxy_port,
        schema=proxy_schema if proxy_schema else schema,
        table=table,
        files=files_list,
    )
    source_names = get_source_names(
        ctx=ctx,
        source_type=source_type,
        dbhost=host,
        dbport=port,
        files=files_list,
    )

    if output == "text":
        # Legacy behavior
        results = post_data_asset_check_requests(
            ctx.obj.client, source_type, source_names, db, schema, schema_contents
        )
        results_string = "\n".join(
            [  # For valid contracts, just print the check mark and name
                f"{EMOJI.GREEN_CHECK.value} {name}" if result[1] == 200 else
                # For missing contracts print a warning
                f"{EMOJI.YELLOW_WARNING.value} {name}:\n\t{result[0]}"
                if result[1] == 404
                else
                # For invalid contracts, print the check results
                f"{EMOJI.RED_X.value} {name}:\n\t{result[0]}"
                for name, result in results.items()
            ]
        )
        # 404s are "OK", treat them as warnings
        if min(map(lambda x: x[1] == 200 or x[1] == 404, results.values())) == False:
            raise click.ClickException(
                f"\n{results_string}\nContract violation(s) found"
            )
        else:
            click.echo(results_string)
            click.echo("No contract violations found")
    else:
        response_type = (
            ResponseType.COMMENT_MARKDOWN
            if output == "markdown"
            else ResponseType.DETAILED
        )
        results = post_data_assets_check_requests(
            ctx.obj.client,
            response_type,
            source_type,
            source_names,
            db,
            schema,
            schema_contents,
        )
        if type(results) == ErrorResponse:
            raise click.ClickException(results.message)
        if response_type == ResponseType.COMMENT_MARKDOWN:
            results = cast(CheckDataAssetCommentMarkdownResponse, results)
            # Only echo the markdown if it's not None or empty, otherwise the stdout will contain a newline
            if results.markdown and results.markdown != "":
                click.echo(results.markdown)
            # Raise an exception if there were errors
            if results.errors:
                errors_string = "\n".join(
                    [json.dumps(error.dict()) for error in results.errors]
                )
                raise click.ClickException(
                    f"{EMOJI.RED_X.value} Contract checking failed for some data assets:\n{errors_string}"
                )
        else:
            results = cast(
                list[
                    CheckDataAssetDetailedResponse
                    | CheckDataAssetErrorResponse
                    | CheckDataAssetNoContractResponse
                ],
                results,
            )
            # Convert the results to dicts by calling Pydantic's json() on each result to deal with enums, which
            # aren't serializable by default
            results_dict = [json.loads(result.json()) for result in results]
            # Check if there were any errors to determine whether to just echo the results or raise an exception
            if any([type(result) == CheckDataAssetErrorResponse for result in results]):
                raise click.ClickException(
                    json.dumps(results_dict, indent=4, sort_keys=True)
                )
            click.echo(json.dumps(results_dict, indent=4, sort_keys=True))
