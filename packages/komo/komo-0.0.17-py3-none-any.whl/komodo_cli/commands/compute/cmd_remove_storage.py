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


@click.command("remove-storage")
@click.option(
    "--storage-type",
    "-s",
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
def cmd_remove_storage(
    ctx: click.Context,
    storage_type: Optional[str],
    s3_bucket: Optional[str],
    manual_confirm: Optional[bool],
):
    compute_dir = get_compute_dir()

    if not os.path.exists(compute_dir):
        printing.error(f"No compute configuration found.", bold=True)
        sys.exit(1)

    try:
        tf_vars = get_vars()
    except Exception as e:
        logger.error(e)
        printing.error(
            f"Error loading {storage_type} for {s3_bucket}",
            bold=True,
        )
        sys.exit(1)

    if storage_type == "fsx":
        fsx_buckets = tf_vars.get("fsx_s3_buckets", [])
        for idx, curr in enumerate(fsx_buckets):
            if s3_bucket == curr:
                fsx_buckets.pop(idx)

        tf_vars["fsx_s3_buckets"] = fsx_buckets
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
            f"Error removing {storage_type} storage for {s3_bucket}",
            bold=True,
        )
        sys.exit(1)

    printing.success(
        f"Storage removed successfully: {storage_type}/{s3_bucket}",
        bold=True,
    )
