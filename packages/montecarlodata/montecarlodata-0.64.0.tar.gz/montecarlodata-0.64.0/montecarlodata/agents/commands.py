import click

from montecarlodata.agents.agent import AgentService
from montecarlodata.agents.fields import (
    DATA_STORE_AGENT,
    GCS,
    REMOTE_AGENT,
    S3,
    GCP,
    AWS,
    AWS_ASSUMABLE_ROLE,
    GCP_JSON_SERVICE_ACCOUNT_KEY,
)
from montecarlodata.collector.commands import NETWORK_TEST_OPTIONS
from montecarlodata.collector.network_tests import CollectorNetworkTestService
from montecarlodata.common import create_mc_client
from montecarlodata.common.commands import DISAMBIGUATE_DC_OPTIONS
from montecarlodata.tools import add_common_options

DRY_RUN_OPTIONS = [
    click.option(
        "--dry-run",
        required=False,
        default=False,
        show_default=True,
        is_flag=True,
        help="Dry run (validates credentials but doesn't create agent).",
    ),
]


@click.group(help="Manage a Monte Carlo Agent.")
def agents():
    """
    Group for any Agent related subcommands
    """
    pass


@agents.command(help="Register a Data Store Agent with remote S3 bucket.")
@click.pass_obj
@click.option(
    "--assumable-role",
    help="ARN of AWS assumable role.",
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of S3 bucket for data store.",
    required=True,
)
@click.option(
    "--external-id",
    help="AWS External ID.",
    required=False,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DISAMBIGUATE_DC_OPTIONS)
def register_s3_store(ctx, bucket_name, **kwargs):
    AgentService(config=ctx["config"], mc_client=create_mc_client(ctx)).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=AWS,
        storage=S3,
        auth_type=AWS_ASSUMABLE_ROLE,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Register a Data Store Agent with Google Cloud Storage.")
@click.pass_obj
@click.option(
    "--key-file",
    help="JSON Key file if auth type is GCP JSON service account key.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of GCS bucket for data store.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DISAMBIGUATE_DC_OPTIONS)
def register_gcs_store(ctx, bucket_name, **kwargs):
    AgentService(config=ctx["config"], mc_client=create_mc_client(ctx)).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=GCP,
        storage=GCS,
        auth_type=GCP_JSON_SERVICE_ACCOUNT_KEY,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Register a Remote GCP Agent.")
@click.pass_obj
@click.option(
    "--key-file",
    help="JSON Key file if auth type is GCP JSON service account key.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--url",
    help="URL for accessing agent.",
    required=True,
)
@add_common_options(DRY_RUN_OPTIONS)
@add_common_options(DISAMBIGUATE_DC_OPTIONS)
def register_gcp_agent(ctx, url, **kwargs):
    AgentService(config=ctx["config"], mc_client=create_mc_client(ctx)).create_agent(
        agent_type=REMOTE_AGENT,
        platform=GCP,
        storage=GCS,
        auth_type=GCP_JSON_SERVICE_ACCOUNT_KEY,
        endpoint=url,
        **kwargs,
    )


@agents.command(help="Deregister an Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent to deregister.", required=True)
def deregister(ctx, agent_id):
    """
    Deregister an Agent (deletes AgentModel from monolith)
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
    ).delete_agent(agent_id)


@agents.command(help="Perform a health check of the Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent.", required=True)
def health(ctx, **kwargs):
    """
    Check the health of an Agent
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
    ).check_agent_health(**kwargs)


@agents.command(help="Upgrades the running version of an Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent to upgrade.", required=True)
@click.option(
    "--image-tag",
    help="Image version to upgrade to.",
    required=False,
)
def upgrade(ctx, **kwargs):
    """
    Performs an upgrade of an Agent
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
    ).upgrade_agent(**kwargs)


@agents.command(help="List all agents in account.", name="list")
@click.pass_obj
@click.option(
    "--show-inactive",
    required=False,
    default=False,
    show_default=True,
    is_flag=True,
    help="Only list active agents.",
)
def list_agents(ctx, **kwargs):
    """
    List all Agents in account
    """
    AgentService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
    ).echo_agents(**kwargs)


@agents.command(help="Checks if telnet connection is usable from the agent.")
@click.pass_obj
@add_common_options(NETWORK_TEST_OPTIONS)
def test_telnet(ctx, **kwargs):
    """
    Network debugging utility to test telnet via the collector
    """
    CollectorNetworkTestService(config=ctx["config"]).echo_telnet_test(**kwargs)


@agents.command(
    help="Tests if a destination exists and accepts requests. "
    "Opens a TCP Socket to a specific port from the agent."
)
@click.pass_obj
@add_common_options(NETWORK_TEST_OPTIONS)
def test_tcp_open(ctx, **kwargs):
    """
    Network debugging utility to test TCP open via the collector
    """
    CollectorNetworkTestService(config=ctx["config"]).echo_tcp_open_test(**kwargs)
