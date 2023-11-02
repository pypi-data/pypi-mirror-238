import json
from typing import Any, Optional, cast

import click
from gable.client import GableClient
from gable.helpers.repo_interactions import get_git_repo_info, get_git_ssh_file_path
from gable.readers.dbapi import DbapiReader
from gable.readers.file import read_file


def standardize_source_type(source_type: str) -> str:
    return source_type.lower()


def validate_db_input_args(user: str, password: str, db: str) -> None:
    if user is None:
        raise ValueError("User (--proxy-user) is required for database connections")
    if password is None:
        raise ValueError(
            "Password (--proxy-password) is required for database connections"
        )
    if db is None:
        raise ValueError("Database (--proxy-db) is required for database connections")


def get_db_connection(
    source_type: str, user: str, password: str, db: str, host: str, port: int
):
    if source_type == "postgres":
        try:
            from gable.readers.postgres import create_postgres_connection

            return create_postgres_connection(user, password, db, host, port)
        except ImportError:
            raise ImportError(
                "The psycopg2 library is not installed. Run `pip install 'gable[postgres]'` to install it."
            )
    elif source_type == "mysql":
        try:
            from gable.readers.mysql import create_mysql_connection

            return create_mysql_connection(user, password, db, host, port)
        except ImportError:
            raise ImportError(
                "The MySQLdb library is not installed. Run `pip install 'gable[mysql]'` to install it."
            )


def get_db_schema_contents(
    connection: Any, schema: str, table: Optional[str] = None
) -> list[dict[str, Any]]:
    reader = DbapiReader(connection=connection)
    return reader.get_information_schema(schema=schema, table=table)  # type: ignore


def get_db_resource_name(
    source_type: str, host: str, port: int, db: str, schema: str, table: str
) -> str:
    return f"{source_type}://{host}:{port}/{db}/{schema}/{table}"


def get_protobuf_resource_name(source_type: str, namespace: str, message: str) -> str:
    return f"{source_type}://{namespace}/{message}"


def get_avro_resource_name(source_type: str, namespace: str, record: str) -> str:
    return f"{source_type}://{namespace}/{record}"


def get_schema_contents(
    source_type: str,
    dbuser: str,
    dbpassword: str,
    db: str,
    dbhost: str,
    dbport: int,
    schema: str,
    table: str,
    files: list[str],
) -> list[str]:
    # Validate the source type arguments and get schema contents
    if source_type in ["postgres", "mysql"]:
        validate_db_input_args(dbuser, dbpassword, db)
        connection = get_db_connection(
            source_type, dbuser, dbpassword, db, dbhost, dbport
        )
        return [json.dumps(get_db_schema_contents(connection, schema, table=table))]
    elif source_type in ["avro", "protobuf", "json_schema"]:
        schema_contents: list[str] = []
        for file in files:
            schema_contents.append(read_file(file))
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")
    return schema_contents


def get_source_names(
    ctx: click.Context,
    source_type: str,
    dbhost: str,
    dbport: int,
    files: list[str],
) -> list[str]:
    # Validate the source type arguments and get schema contents
    if source_type in ["postgres", "mysql"]:
        return [f"{dbhost}:{dbport}"]
    elif source_type in ["avro", "protobuf", "json_schema"]:
        source_names = []
        for file in files:
            source_names.append(get_git_ssh_file_path(get_git_repo_info(file), file))
        return source_names
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")


def send_schemas_to_gable(
    client: GableClient,
    source_type: str,
    source_names: list[str],
    database_schema: str,
    schema_contents: list[str],
) -> tuple[dict[str, Any], bool, int]:
    result, success, status_code = client.post(
        "v0/data-asset/ingest",
        json={
            "sourceType": source_type,
            "sourceNames": source_names,
            "databaseSchema": database_schema,
            "schema": schema_contents,
        },
    )
    return cast(dict[str, Any], result), success, status_code
