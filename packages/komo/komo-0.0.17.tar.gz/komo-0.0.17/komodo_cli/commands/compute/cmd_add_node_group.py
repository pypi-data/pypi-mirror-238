import os
import sys

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (get_compute_dir, get_vars,
                                               get_vars_filepath, run_cmd,
                                               update_vars)
from komodo_cli.utils import handle_errors


@click.command("add-node-group")
@click.option(
    "--node-group-name",
    "-n",
    type=str,
    required=True,
    default=None,
    help="Name of the node group to add.",
)
@click.option(
    "--instance-type",
    "-t",
    type=str,
    required=True,
    default=None,
    help="Instance type to add.",
)
@click.option(
    "--instance-max-count",
    "-c",
    type=int,
    required=True,
    default=None,
    help="Maximum number of this instance type to allow.",
)
@click.option(
    "--manual_confirm",
    "-m",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="Manually confirm terraform plan.",
)
@click.pass_context
@handle_errors
def cmd_add_node_group(
    ctx: click.Context,
    node_group_name: str,
    instance_type: str,
    instance_type_max_count: int,
    manual_confirm: bool,
):
    """
    Add a node group to your compute cluster. This only works for Kubernetes compute clusters create with `komo compute create`.
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

    if "node_groups" not in tf_vars:
        tf_vars["node_groups"] = {}

    tf_vars["node_groups"][node_group_name] = {
        "instance_type": instance_type,
        "max_count": instance_type_max_count,
    }
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
            f"Error adding node group {node_group_name}",
            bold=True,
        )
        sys.exit(1)

    printing.success(
        f"Successfully added node group {node_group_name}",
        bold=True,
    )
