import os
import sys

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (get_compute_dir, get_vars,
                                               get_vars_filepath, run_cmd,
                                               update_vars)
from komodo_cli.utils import handle_errors


@click.command("remove-node-group")
@click.option(
    "--node-group-name",
    "-n",
    type=str,
    required=True,
    default=None,
    help="Name of the node group to remove.",
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
def cmd_remove_node_group(
    ctx: click.Context,
    node_group_name: str,
    manual_confirm: bool,
):
    """
    Remove a node group from your compute cluster. This only works for Kubernetes compute clusters create with `komo compute create`.
    """
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

    if node_group_name not in tf_vars["node_groups"]:
        printing.error(
            f"Node group {node_group_name} not found in compute configuration.",
            bold=True,
        )
        sys.exit(1)

    tf_vars["node_groups"].pop(node_group_name)
    update_vars(tf_vars)

    cmd = [
        "terraform",
        f"-chdir={compute_dir}",
        "apply",
        f"-var-file={get_vars_filepath()}",
    ]

    if not manual_confirm:
        cmd.append("-auto-approve")

    exit_code, _, stderr = run_cmd(" ".join(cmd))
    if exit_code != 0:
        logger.error(stderr)
        printing.error(
            f"Error removing node group {node_group_name}",
            bold=True,
        )
        sys.exit(1)

    printing.success(
        f"Successfully removed node group {node_group_name}.",
        bold=True,
    )
