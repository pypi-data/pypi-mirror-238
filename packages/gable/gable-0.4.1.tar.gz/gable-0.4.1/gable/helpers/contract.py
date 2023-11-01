import os
from typing import Any, Dict, List

import click
from gable.helpers.repo_interactions import get_git_repo_info
from gable.openapi import ContractInput, NotificationLevel, PostContractRequest, Status


def load_contract_from_file(file: click.File) -> Dict[str, Any]:
    if file.name.endswith(".yaml") or file.name.endswith(".yml"):
        import yaml

        try:
            return yaml.safe_load(file)  # type: ignore
        except yaml.scanner.ScannerError as exc:  # type: ignore
            # This should be a custom exception for user errors
            raise click.ClickException(f"Error parsing YAML file: {file.name}")
    elif file.name.endswith(".toml"):
        raise click.ClickException(
            "We don't currently support defining contracts with TOML, try YAML instead!"
        )
    elif file.name.endswith(".json"):
        raise click.ClickException(
            "We don't currently support defining contracts with JSON, try YAML instead!"
        )
    else:
        raise click.ClickException("Unknown filetype, try YAML instead!")


def contract_files_to_post_contract_request(
    contract_files: List[click.File],
) -> PostContractRequest:
    contracts = []
    for contract_file in contract_files:
        contract = load_contract_from_file(contract_file)
        if "id" not in contract:
            raise click.ClickException(f"{contract_file}:\n\tContract must have an id.")
        git_info = get_git_repo_info(contract_file.name)
        relative_path = os.path.relpath(
            contract_file.name, git_info["localRepoRootDir"]
        )
        if relative_path.startswith(".."):
            raise click.ClickException(
                f"{contract_file.name}:\n\tContract must be located within the git repo where gable is being executed ({git_info['localRepoRootDir']})."
            )
        contract_input = ContractInput(
            id=contract["id"],
            version="0.0.1",  # This should be server calculated
            status=Status("ACTIVE"),
            reviewers=[],  # This should be info accessible from a github PR integration
            filePath=relative_path,
            contractSpec=contract,
            gitHash=git_info["gitHash"],
            gitRepo=git_info["gitRemoteOriginHTTPS"],  # type: ignore
            gitUser=git_info["gitUser"],
            mergedAt=git_info["mergedAt"],
            notificationLevel=NotificationLevel.INACTIVE,
        )
        contracts.append(contract_input)
    return PostContractRequest(
        __root__=contracts,
    )
