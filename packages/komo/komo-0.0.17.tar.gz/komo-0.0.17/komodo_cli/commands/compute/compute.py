import click

from komodo_cli.commands.compute.cmd_add_node_group import cmd_add_node_group
from komodo_cli.commands.compute.cmd_add_storage import cmd_add_storage
from komodo_cli.commands.compute.cmd_create import cmd_create
from komodo_cli.commands.compute.cmd_list import cmd_list
from komodo_cli.commands.compute.cmd_remove_node_group import \
    cmd_remove_node_group
from komodo_cli.commands.compute.cmd_remove_storage import cmd_remove_storage
from komodo_cli.commands.compute.cmd_terminate import cmd_terminate


@click.group()
@click.pass_context
def compute(ctx: click.Context):
    """Manage Komodo compute"""
    pass


compute.add_command(cmd_create)
compute.add_command(cmd_list)
compute.add_command(cmd_terminate)
compute.add_command(cmd_add_storage)
compute.add_command(cmd_remove_storage)
compute.add_command(cmd_add_node_group)
compute.add_command(cmd_remove_node_group)
