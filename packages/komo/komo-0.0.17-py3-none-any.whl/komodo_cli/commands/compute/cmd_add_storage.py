import os
import sys
from typing import Optional

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (get_compute_dir, get_vars,
                                               get_vars_filepath, run_cmd,
                                               update_vars)
from komodo_cli.utils import handle_errors


@click.command("add-storage")
@click.option(
    "--storage-type",
    "-t",
    type=str,
    default="fsx",
    help="Storage type to add.",
)
@click.option(
    "--s3-bucket",
    type=str,
    required=True,
    default=None,
    help="Name of the S3 bucket backing the storage",
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
def cmd_add_storage(
    ctx: click.Context,
    storage_type: Optional[str],
    s3_bucket: Optional[str],
    manual_confirm: Optional[bool],
):
    """
    Add a storage backend to your compute cluster. This only works for Kubernetes compute clusters create with `komo compute create`.
    """
    compute_dir = get_compute_dir()

    if not os.path.exists(compute_dir):
        printing.error(f"No compute configuration found.", bold=True)
        sys.exit(1)

    try:
        tf_vars = get_vars()
    except Exception as e:
        logger.error(e)
        printing.error(
            f"Error loading tf vars",
            bold=True,
        )
        sys.exit(1)

    info_message_source = ""
    if storage_type == "fsx":
        fsx_s3_buckets = tf_vars.get("fsx_s3_buckets", [])
        fsx_s3_buckets.append(s3_bucket)
        tf_vars["fsx_s3_buckets"] = fsx_s3_buckets
        update_vars(tf_vars)
        info_message_source = f"fsx-claim-{s3_bucket}"

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
            f"Error adding {storage_type} storage for {s3_bucket}",
            bold=True,
        )
        sys.exit(1)

    printing.error(
        f"Storage added successfully: {storage_type}/{s3_bucket}",
        bold=True,
    )

    printing.header(
        f"Add the following to your backend's mounts section",
        bold=True,
    )
    printing.info(
        f"""
mounts:
  - source: {info_message_source}
    target: /desired-path
    type: volume
"""
    )
