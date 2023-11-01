import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import (
    List,
    Optional,
)
from urllib.parse import urljoin

import click
import questionary
import requests
from dataclasses_json import (
    DataClassJsonMixin,
    Undefined,
    dataclass_json,
)
from pycarlo.core import (
    Client,
    Mutation,
    Query,
)
from tabulate import tabulate

from montecarlodata import settings
from montecarlodata.agents.fields import (
    GCP_JSON_SERVICE_ACCOUNT_KEY,
    AWS_ASSUMABLE_ROLE,
)
from montecarlodata.common.common import read_as_json_string
from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors, complain_and_abort

DOCKER_HUB_TAGS_PAGE_SIZE = 10
DOCKER_HUB_TAGS_BASE_URL = "https://hub.docker.com/v2/namespaces/"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass()
class DockerTag(DataClassJsonMixin):
    name: str
    last_updated: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass()
class DockerTagsResult(DataClassJsonMixin):
    results: List[DockerTag]


class AgentService:
    _AGENT_FRIENDLY_HEADERS = [
        "Agent ID",
        "Agent Type / Platform",
        "DC ID",
        "Endpoint",
        "Version",
        "Last updated (UTC)",
        "Active",
    ]
    _VALIDATION_RESPONSE_HEADERS = [
        "Message",
        "Cause",
        "Resolution",
    ]

    def __init__(
        self,
        config: Config,
        mc_client: Client,
        user_service: Optional[UserService] = None,
    ):
        self._abort_on_error = True
        self._mc_client = mc_client
        self._user_service = user_service or UserService(config=config)
        self._image_org = config.mcd_agent_image_org
        self._image_repo = config.mcd_agent_image_repo
        self._image_name = (
            f"{config.mcd_agent_image_host}/{self._image_org}/{self._image_repo}"
        )

    @manage_errors
    def create_agent(
        self, agent_type, platform, storage, auth_type, endpoint, **kwargs
    ) -> None:
        """
        Register an agent by validating connection and creating an AgentModel in the monolith.
        """

        dry_run = kwargs.get("dry_run", False)
        agent_request = {
            "agent_type": agent_type,
            "endpoint": endpoint,
            "storage_type": storage,
            "platform": platform,
            "auth_type": auth_type,
            "dry_run": dry_run,
        }

        if kwargs.get("dc_id"):
            agent_request["data_collector_id"] = kwargs["dc_id"]

        if auth_type == GCP_JSON_SERVICE_ACCOUNT_KEY:
            agent_request["credentials"] = read_as_json_string(kwargs["key_file"])
        elif auth_type == AWS_ASSUMABLE_ROLE:
            creds = {"aws_assumable_role": kwargs["assumable_role"]}
            if kwargs["external_id"]:
                creds["external_id"] = kwargs["external_id"]
            agent_request["credentials"] = json.dumps(creds)

        mutation = Mutation()
        # the trailing call to __fields__ is needed to force selection of all possible fields
        mutation.create_or_update_agent(**agent_request).__fields__()
        result = self._mc_client(mutation).create_or_update_agent

        self._validate_response(result.validation_result)

        if result.agent_id is not None:
            click.echo("Agent successfully registered!\n" f"AgentId: {result.agent_id}")
        elif dry_run:
            if result.validation_result.success:
                click.echo("Dry run completed successfully!")
            else:
                complain_and_abort("Dry run failed.")
        else:
            complain_and_abort("Failed to register agent.")

    @manage_errors
    def delete_agent(self, agent_id) -> None:
        """
        Deregister an Agent (deletes AgentModel from monolith)
        """
        variables = dict(agent_id=agent_id)

        mutation = Mutation()
        mutation.delete_agent(**variables)
        result = self._mc_client(mutation).delete_agent

        if result.success:
            click.echo(f"Agent {agent_id} deregistered.")
        else:
            complain_and_abort("Failed to deregister agent.")

    @manage_errors
    def echo_agents(
        self,
        show_inactive: bool = False,
        headers: Optional[str] = "firstrow",
        table_format: Optional[str] = "fancy_grid",
    ):
        """
        Display agents in an easy-to-read table.
        """

        table = [self._AGENT_FRIENDLY_HEADERS]
        for agent in self._user_service.agents:
            is_active = not agent.get("isDeleted")
            if not show_inactive and not is_active:
                continue
            full_type = f"{agent.get('agentType', '')} / {agent.get('platform', '')}"
            last_updated = (
                datetime.fromisoformat(agent.get("lastUpdatedTime")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if agent.get("lastUpdatedTime")
                else "-"
            )

            table += [
                [
                    agent.get("uuid") or "",
                    full_type,
                    agent.get("dc_id") or "",
                    agent.get("endpoint") or "",
                    agent.get("imageVersion") or "-",
                    last_updated,
                    is_active,
                ]
            ]

        # If the account has no agents, add 1 line of empty values so tabulate() creates a pretty
        # empty table
        if len(table) == 1:
            table += ["" for _ in self._AGENT_FRIENDLY_HEADERS]

        click.echo(
            tabulate(table, headers=headers, tablefmt=table_format, maxcolwidths=100)
        )

    def _validate_response(self, validation_result):
        table = [self._VALIDATION_RESPONSE_HEADERS]
        stack_trace = None

        if validation_result.errors:
            for error in validation_result.errors:
                stack_trace = f"-----------\n{error.stack_trace}\n"

                table += [
                    [
                        click.style(f"ERROR: {error.friendly_message or ''}", fg="red"),
                        error.cause or "",
                        error.resolution or "",
                    ]
                ]

        if validation_result.warnings:
            for warning in validation_result.warnings:
                table += [
                    [
                        click.style(
                            f"WARNING: {warning.friendly_message or ''}", fg="yellow"
                        ),
                        warning.cause or "",
                        warning.resolution or "",
                    ]
                ]

        # If there are any errors or warnings returned, display them
        if len(table) > 1:
            click.echo(
                tabulate(
                    table, headers="firstrow", tablefmt="fancy_grid", maxcolwidths=100
                )
            )

        # If Verbose Errors is set as env variable and there was an error stack trace, save trace
        # to a file and print path
        if settings.MCD_VERBOSE_ERRORS and stack_trace:
            stack_trace_filename = f"mcd_error_trace_{uuid.uuid4()}.txt"
            with open(stack_trace_filename, "w") as stack_trace_file:
                stack_trace_file.write(stack_trace)
            click.echo(f"Stack Trace of error(s) saved to /{stack_trace_filename}")

    @manage_errors
    def check_agent_health(self, **kwargs):
        storage_query = Query()
        storage_query.test_data_store_reachability(**kwargs)
        storage_result = self._mc_client(
            storage_query,
            idempotent_request_id=str(uuid.uuid4()),
            timeout_in_seconds=40,  # let Monolith timeout first
        ).test_data_store_reachability

        if not storage_result.success:
            return self._validate_response(storage_result)
        agent = self._user_service.get_agent(**kwargs)
        if agent.get("agentType") != "REMOTE_AGENT":
            return click.echo("Agent health check succeeded!")

        agent_query = Query()
        agent_query.test_agent_reachability(**kwargs)
        agent_result = self._mc_client(
            agent_query,
            idempotent_request_id=str(uuid.uuid4()),
            timeout_in_seconds=40,  # let Monolith timeout first
        ).test_agent_reachability

        if agent_result.success:
            if agent_result.additional_data.returned_data:
                headers = []
                rows = []
                for field, value in agent_result.additional_data.returned_data.items():
                    headers.append(field)
                    rows.append(value)
                click.echo(
                    tabulate(
                        [rows], headers=headers, tablefmt="fancy_grid", maxcolwidths=100
                    )
                )
            return click.echo("Agent health check succeeded!")

        return self._validate_response(agent_result)

    @manage_errors
    def upgrade_agent(self, **kwargs):
        image_tag = self._choose_image_tag(**kwargs)
        if not image_tag:
            # user canceled prompt without choosing a response
            raise click.Abort()
        image = f"{self._image_name}:{image_tag}"
        click.echo(f"Upgrading agent with image '{image}'")
        variables = {
            "agent_id": kwargs["agent_id"],
            "image": image,
        }

        mutation = Mutation()
        mutation.upgrade_agent(**variables)
        result = self._mc_client(
            mutation,
            idempotent_request_id=str(uuid.uuid4()),
            timeout_in_seconds=40,  # let Monolith timeout first
        ).upgrade_agent

        click.echo("Upgrade succeeded!")
        if result.upgrade_result:
            headers = []
            rows = []
            for field, value in result.upgrade_result.items():
                headers.append(field)
                rows.append(value)
            headers = list(result.upgrade_result.keys())
            rows = result.upgrade_result.values()
            click.echo(
                tabulate(
                    [rows], headers=headers, tablefmt="fancy_grid", maxcolwidths=100
                )
            )

    def _choose_image_tag(
        self, agent_id: str, image_tag: Optional[str] = None
    ) -> Optional[str]:
        if image_tag and self._validate_tag(image_tag):
            return image_tag

        versions = self._get_recent_versions()
        if not image_tag:
            # choose latest version based on agent platform
            agent = self._user_service.get_agent(agent_id)
            platform = agent.get("platform")
            image_variant = "cloudrun" if platform == "GCP" else "generic"
            click.echo(
                f"Defaulting to {image_variant} image variants because platform is {platform}"
            )
            versions_with_variant = [
                version for version in versions if image_variant in version
            ]
            if versions_with_variant:
                return versions_with_variant[0]
        return questionary.select(
            "Please choose a valid image tag", choices=versions
        ).ask()

    def _validate_tag(self, image_tag: str) -> bool:
        image_path = f"{self._image_org}/repositories/{self._image_repo}"
        url: str = urljoin(DOCKER_HUB_TAGS_BASE_URL, f"{image_path}/tags/{image_tag}")
        response = requests.head(url=url)
        return response.status_code == 200

    def _get_recent_versions(self) -> List[str]:
        image_path = f"{self._image_org}/repositories/{self._image_repo}"
        url = urljoin(
            DOCKER_HUB_TAGS_BASE_URL,
            f"{image_path}/tags?page_size={DOCKER_HUB_TAGS_PAGE_SIZE}&page=1",
        )
        response = requests.get(url=url)
        response.raise_for_status()
        payload: DockerTagsResult = DockerTagsResult.from_json(response.text)
        payload.results.sort(key=lambda t: t.last_updated, reverse=True)
        return [tag.name for tag in payload.results if "latest" not in tag.name]
