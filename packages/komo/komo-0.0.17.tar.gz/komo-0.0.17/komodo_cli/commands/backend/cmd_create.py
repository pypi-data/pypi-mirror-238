import os

import click

import komodo_cli.printing as printing
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.utils import APIClient, handle_errors


@click.command("create")
@click.option(
    "--name",
    "-n",
    type=str,
    default=None,
    help="Name of the backend to create",
)
@click.option(
    "--backend-type",
    "-t",
    type=click.Choice(list(BackendFactory.backend_types.keys())),
    help="Type of backend to create.",
    required=True,
)
@click.pass_context
@handle_errors
def cmd_create(
    ctx: click.Context,
    name: str,
    backend_type: str,
):
    api_client: APIClient = ctx.obj["api_client"]

    backend_cls = BackendFactory.backend_types[backend_type]

    config_params = backend_cls.config_params
    config = {}
    for param in config_params:
        while True:
            value = click.prompt(param.name, default=None, type=param.dtype)

            if param.read_from_file:
                if not os.path.isfile(value):
                    printing.error(f"{value} is not a valid file")
                    continue

                with open(value, "r") as f:
                    value = f.read()

            break

        config[param.name] = value

    api_client.create_backend(
        name,
        backend_type,
        config,
    )

    printing.success(f"Backend '{name}' succesfully created")
