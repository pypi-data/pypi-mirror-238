import json
import os
import sys
from collections import defaultdict

import click
from loguru import logger
from tabulate import tabulate

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import get_compute_dir, print_clusters
from komodo_cli.utils import handle_errors


@click.command("list")
@click.pass_context
@handle_errors
def cmd_list(ctx: click.Context):
    """List Komodo computes"""
    compute_dir = get_compute_dir()

    if not os.path.exists(compute_dir):
        printing.error(f"No compute configuration found.", bold=True)
        sys.exit(1)
    else:
        print_clusters()
