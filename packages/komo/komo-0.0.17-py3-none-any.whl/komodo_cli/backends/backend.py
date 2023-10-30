import abc
from abc import ABC
from typing import Dict, NamedTuple, Tuple

from komodo_cli.types import Backend as BackendSchema
from komodo_cli.types import ClientException, Job, JobStatus, Machine
from komodo_cli.utils import APIClient


class ConfigParam(NamedTuple):
    name: str
    dtype: type
    description: str
    required: bool
    read_from_file: bool = False


class Backend(ABC):
    def __init__(self, name: str, api_client: APIClient, config: Dict, resources: Dict):
        self.name = name
        self.api_client: APIClient = api_client
        self.config = config
        self.resources = resources

    # The params expected in the config for the backend (eg. credentials)
    config_params: Tuple[ConfigParam, ...]
    # The keys expected in the configs of the resources added to the backend (eg. num gpus)
    resource_config_params: Tuple[ConfigParam, ...]

    @abc.abstractmethod
    def run(
        self,
        command: Tuple[str],
        num_nodes: int,
        resource_name: str,
        image: str,
        env: Dict[str, str],
        mounts: list,
        workdir: str,
    ) -> Job:
        pass

    @abc.abstractmethod
    def create_machine(
        self,
        machine_name: str,
        resource_name: dict,
        image: str,
        env: Dict[str, str],
        mounts: list,
        workdir: str,
    ) -> Machine:
        pass

    @abc.abstractmethod
    def logs(self, job_id: str, node_index: int, watch: bool):
        pass

    @abc.abstractmethod
    def shell(self, job_id: str, node_index: int):
        pass

    def vscode(self, job_id: str, node_index: int):
        raise ClientException(
            "Support for VSCode for this type of backend is not supported yet, but coming soon!"
        )

    @abc.abstractmethod
    def cancel(self, job_id: str):
        pass

    @abc.abstractmethod
    def delete(self, job_id: str):
        pass

    @abc.abstractstaticmethod
    def supports_shell() -> bool:
        pass
