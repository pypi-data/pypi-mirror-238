import os
import sys
from typing import Optional

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (SUPPORTED_COMPUTE_SERVICES,
                                               get_compute_dir, get_vars,
                                               get_vars_filepath, run_cmd)
from komodo_cli.utils import handle_errors


@click.command("terminate")
@click.option(
    "--compute-type",
    "-t",
    type=str,
    default="eks",
    help="The type of compute infrastructure type to destroy.",
)
@click.option(
    "--name",
    "-n",
    type=str,
    required=True,
    help="The name of the compute infrastructure to destroy",
)
@click.option(
    "--manual-confirm",
    "-m",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="Manually confirm terraform plan.",
)
@click.pass_context
@handle_errors
def cmd_terminate(
    ctx: click.Context,
    compute_type: Optional[str],
    name: Optional[str],
    manual_confirm: Optional[bool],
):
    """Destroy Komodo compute"""
    if compute_type not in SUPPORTED_COMPUTE_SERVICES:
        printing.error(
            f"Unsupported compute type {compute_type}. Supported compute types: {SUPPORTED_COMPUTE_SERVICES}",
            bold=True,
        )
        sys.exit(1)

    compute_dir = get_compute_dir()

    if not os.path.exists(compute_dir):
        printing.error(f"No compute configuration found.", bold=True)
        sys.exit(1)

    try:
        tf_vars = get_vars()
    except Exception as e:
        logger.error(e)
        printing.error(f"Error loading tf vars", bold=True)
        sys.exit(1)

    if tf_vars["eks_cluster_id"][1:-1] != name:
        printing.error(
            f"Cluster ID {name} does not match the cluster ID in the configuration {tf_vars['eks_cluster_id']}",
            bold=True,
        )
        sys.exit(1)

    cmd = [
        "terraform",
        f"-chdir={compute_dir}",
        "destroy",
        f"-var-file={get_vars_filepath()}",
    ]

    if not manual_confirm:
        cmd.append("-auto-approve")

    exit_code, _, stderr = run_cmd(" ".join(cmd))
    if exit_code != 0:
        logger.error(stderr)
        printing.error("Error destroying compute", bold=True)
        sys.exit(1)

    os.remove(get_vars_filepath())
    printing.success("Compute destroyed successfully", bold=True)
    # TODO: delete backend from server via api call.
