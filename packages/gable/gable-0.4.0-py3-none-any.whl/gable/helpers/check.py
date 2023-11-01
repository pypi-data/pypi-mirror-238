import json
from typing import Annotated, Any, List, Optional, Tuple, Union, cast

import click
from gable.client import GableClient
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetNoContractResponse,
    CheckDataAssetRequest,
    CheckDataAssetsRequest,
    ErrorResponse,
    Input,
    ResponseType,
)
from gable.readers.dbapi import DbapiReader
from gable.readers.file import read_file
from pydantic import Field, parse_obj_as

# Discriminated union for the response from the /data-assets/check endpoint
CheckDataAssetDetailedResponseUnion = Annotated[
    Union[
        CheckDataAssetDetailedResponse,
        CheckDataAssetErrorResponse,
        CheckDataAssetNoContractResponse,
    ],
    Field(discriminator="responseType"),
]


def post_contract_check_request(
    client: GableClient,
    contract_id: str,
    source_type: str,
    schema_contents: str,
) -> tuple[str, bool]:
    result, success, status_code = client.post(
        f"v0/contract/{contract_id}/check",
        json={
            "sourceType": source_type,
            "schemaContents": schema_contents,
        },
    )
    return str(cast(dict[str, Any], result)["message"]), success


def post_data_asset_check_requests(
    client: GableClient,
    source_type: str,
    source_names: List[str],
    realDbName: str,
    realDbSchema: str,
    schema_contents: List[str],
) -> dict[str, Tuple[str, int]]:
    results: dict[str, Tuple[str, int]] = {}
    requests = get_check_data_asset_requests(
        source_type=source_type,
        source_names=source_names,
        schema_contents=schema_contents,
        realDbName=realDbName,
        realDbSchema=realDbSchema,
    )
    for source_name, request in requests.items():
        result, success, status_code = client.post(
            "v0/data-asset/check",
            json=request.dict(),
        )
        results[source_name] = (
            cast(dict[str, Any], result)["message"],
            status_code,
        )
    return results


def post_data_assets_check_requests(
    client: GableClient,
    responseType: ResponseType,
    source_type: str,
    source_names: List[str],
    realDbName: str,
    realDbSchema: str,
    schema_contents: List[str],
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[
        Union[
            CheckDataAssetDetailedResponse,
            CheckDataAssetErrorResponse,
            CheckDataAssetNoContractResponse,
        ]
    ],
]:
    requests = get_check_data_asset_requests(
        source_type=source_type,
        source_names=source_names,
        schema_contents=schema_contents,
        realDbName=realDbName,
        realDbSchema=realDbSchema,
    )
    inputs = [Input.parse_obj(request.dict()) for request in requests.values()]
    request = CheckDataAssetsRequest(
        responseType=responseType,
        inputs=inputs,
    )
    result, success, status_code = client.post(
        "v0/data-assets/check",
        json=json.loads(request.json()),
    )
    if responseType == ResponseType.DETAILED:
        if type(result) == list:
            return [
                parse_obj_as(
                    CheckDataAssetDetailedResponse
                    | CheckDataAssetErrorResponse
                    | CheckDataAssetNoContractResponse,
                    r,
                )
                for r in result
            ]
        else:
            return ErrorResponse.parse_obj(result)
    else:
        return parse_obj_as(
            CheckDataAssetCommentMarkdownResponse | ErrorResponse, result
        )


def get_check_data_asset_requests(
    source_type: str,
    source_names: list[str],
    schema_contents: list[str],
    realDbName: Optional[str] = None,
    realDbSchema: Optional[str] = None,
) -> dict[str, CheckDataAssetRequest]:
    requests: dict[str, CheckDataAssetRequest] = {}
    # If this is a database, there might be multiple table's schemas within the information schema
    # returned from the DbApi reader. In that case, we need to post each table's schema separately.
    if source_type in ["postgres", "mysql"]:
        schema_contents_str = schema_contents[0]
        source_name = source_names[0]
        information_schema = json.loads(schema_contents_str)
        grouped_table_schemas: dict[str, List[Any]] = {}
        for information_schema_row in information_schema:
            if information_schema_row["TABLE_NAME"] not in grouped_table_schemas:
                grouped_table_schemas[information_schema_row["TABLE_NAME"]] = []
            grouped_table_schemas[information_schema_row["TABLE_NAME"]].append(
                information_schema_row
            )
        for table_name, table_schema in grouped_table_schemas.items():
            requests[
                f"{realDbName}.{realDbSchema}.{table_name}"
            ] = CheckDataAssetRequest(
                sourceType=source_type,
                sourceName=source_name,
                realDbName=realDbName,
                realDbSchema=realDbSchema,
                schemaContents=json.dumps(table_schema),
            )
    else:
        for source_name, schema in zip(source_names, schema_contents):
            requests[source_name] = CheckDataAssetRequest(
                sourceType=source_type,
                sourceName=source_name,
                schemaContents=schema,
            )
    return requests
