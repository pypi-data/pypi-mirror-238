import os
import time
from typing import Optional

import click
from loguru import logger
from vyper import Vyper

import komodo_cli.printing as printing
from komodo_cli.backends.backend import Backend
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.overlay_images.overlay_images import OverlayImages
from komodo_cli.types import JobStatus
from komodo_cli.utils import (
    APIClient, config_args_to_dict, handle_errors,
    update_context_project_config_with_backend_override,
    update_context_with_project_config, validate_backend_config,
    validate_overlay_images_repository)


@click.command("create")
@click.argument(
    "name",
    type=str,
)
@click.option(
    "--backend",
    "-b",
    type=str,
    default=None,
    help="Name of the backend to use.",
)
@click.option(
    "--resource",
    "-r",
    type=str,
    default=None,
    help="Resource type to use for the job as defined in the config file. Ignored for local jobs.",
)
@click.option(
    "--config",
    "-c",
    type=str,
    default="",
    help=(
        "Override any parameters in the section of your project config corresponding to the specified backend."
        "Values must be provided as a comma-separated list of key=value pairs."
    ),
)
@click.option("--detach", "-d", is_flag=True)
@click.pass_context
@handle_errors
def cmd_create(
    ctx: click.Context,
    name: str,
    backend: Optional[str],
    resource: Optional[str],
    config: str,
    detach: bool,
):
    backend_name = backend
    update_context_with_project_config(ctx)
    api_client: APIClient = ctx.obj["api_client"]

    project_config: Vyper = ctx.obj["project_config"]
    if backend_name is None:
        backend_name = project_config.get("default_backend")
        if backend_name is None:
            printing.error("No backend was specified", bold=True)
            exit(1)

    backend_config_override = config_args_to_dict(config)
    update_context_project_config_with_backend_override(
        ctx, backend_name, backend_config_override
    )
    project_backend_config = project_config.get("configs")[backend_name]
    try:
        validate_backend_config(backend_name, project_backend_config)
    except Exception as e:
        printing.error(f"Error while validating backend config: {str(e)}", bold=True)
        exit(1)

    backend_schema = api_client.get_backend(backend_name)
    backend: Backend = BackendFactory.get_backend(
        backend_schema,
        api_client,
    )

    if resource is None:
        resource = project_backend_config.get("default_resource")
        if resource is None:
            # resource not needed for local backend
            if backend_schema.type != "local":
                printing.error("No resource was specified", bold=True)
                exit(1)

    logger.info(f"Using backend {backend_name}")
    logger.info(f"Resource: {resource}")

    if not backend.supports_shell():
        printing.error(
            f"Backend {backend_name} does not support machines",
            bold=True,
        )
        return

    workspace = project_backend_config.get("workspace", os.getcwd())
    if workspace:
        try:
            validate_overlay_images_repository(project_config)
        except Exception as e:
            printing.error(
                f"Error while validating overlay images repository: {str(e)}",
                bold=True,
            )
            exit(1)

        o = OverlayImages(
            project_backend_config["image"],
            workspace,
            project_backend_config.get("workdir"),
            project_config.get("overlay_images_repository"),
        )

        printing.info("Building an overlay image", bold=True)
        overlay_image = o.build_overlay_image()

        printing.info("Pushing an overlay image", bold=True)
        o.push_overlay_image(overlay_image)
        project_backend_config["image"] = overlay_image.tags[0]

    printing.header("Starting a machine", bold=True)
    machine = backend.create_machine(
        name,
        resource,
        project_backend_config["image"],
        project_backend_config["env"],
        project_backend_config["mounts"],
        project_backend_config["workdir"],
    )

    printing.success(
        f"Created a machine on backend {machine.backend_name} with name {machine.name}",
        bold=True,
    )

    if detach:
        return

    printing.success("Waiting for machine to start...", bold=True)

    while True:
        machine = api_client.get_machine(name)
        status = machine.status
        if status != JobStatus.PENDING:
            break
        time.sleep(1)

    backend.shell(machine.backend_job_id, 0)
