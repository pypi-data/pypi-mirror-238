import os
import subprocess
import tempfile
from typing import Dict, Tuple

import boto3
import botocore
from loguru import logger

from komodo_cli.backends.backend import Backend, ConfigParam
from komodo_cli.types import ClientException, Job, Machine
from komodo_cli.utils import APIClient


class AWSBatchBackend(Backend):
    config_params = (
        ConfigParam("access_key_id", str, "AWS access key ID", True),
        ConfigParam("secret_access_key", str, "AWS secret access key", True),
        ConfigParam("region", str, "AWS region", True),
        ConfigParam(
            "ssh-key",
            str,
            "Path to the ssh key needed to allow ssh access to the EC2 instances",
            True,
            True,
        ),
    )
    resource_config_params = (
        ConfigParam("instance_type", str, "instance type", True),
        ConfigParam("queue", str, "name of the queue", True),
    )

    def __init__(self, name: str, api_client: APIClient, config: Dict, resources: Dict):
        super().__init__(name, api_client, config, resources)

        session = boto3.Session(
            region_name=config["region"],
        )
        self._batch_client = session.client("batch", region_name=config["region"])
        self._ec2_client = session.client("ec2", region_name=config["region"])
        self._logs_client = session.client("logs", region_name=config["region"])
        self._ecs_client = session.client("ecs", region_name=config["region"])

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
        job = self.api_client.create_job(
            self.name,
            command,
            num_nodes,
            image,
            env,
            mounts,
            workdir,
            resource_name,
        )

        return job

    def create_machine(
        self,
        machine_name: str,
        resource_name: str,
        image: str,
        env: Dict[str, str],
        mounts: list,
        workdir: str,
    ) -> Machine:
        machine = self.api_client.create_machine(
            machine_name,
            self.name,
            image,
            env,
            mounts,
            workdir,
            resource_name,
        )
        return machine

    def _get_job(self, job_id: str, node_index: int) -> dict:
        job_id = f"{job_id}#{node_index}"
        try:
            jobs = self._batch_client.describe_jobs(jobs=[job_id])["jobs"]
            if len(jobs) == 0:
                raise ClientException(f"AWS Batch job {job_id} not found")

            assert len(jobs) == 1
            job = jobs[0]

            return job
        except botocore.exceptions.ClientError as err:
            logger.error(str(err))
            raise err

    def logs(self, job_id: str, node_index: int, watch: bool):
        job = self._get_job(job_id, node_index)

        if job.get("status", None) == "RUNNING":
            log_stream_name = job["container"]["logStreamName"]
        else:
            attempts = job["attempts"]
            if len(attempts) == 0:
                return

            attempt = attempts[-1]
            container = attempt["container"]
            log_stream_name = container["logStreamName"]

        next_token = None

        while True:
            args = {}
            if next_token is not None:
                args["nextToken"] = next_token

            try:
                response = self._logs_client.get_log_events(
                    logGroupName="/aws/batch/job",
                    logStreamName=log_stream_name,
                    limit=10000,
                    startFromHead=True,
                    **args,
                )
            except self._logs_client.exceptions.ResourceNotFoundException:
                return
            if response["nextForwardToken"] == next_token:
                # we've reached the end of the available logs

                # if watch is False, then we end here
                if not watch:
                    break

                # if the job is running, we wait for more logs
                job = self._get_job(job_id, node_index)
                if job["status"] == "RUNNING":
                    continue

                # if the job is not running, then we end here
                break

            next_token = response["nextForwardToken"]

            for event in response["events"]:
                yield event["message"] + "\n"

    def shell(self, job_id: str, node_index: int):
        job = self._get_job(job_id, node_index)
        status = job["status"]
        if status != "RUNNING":
            raise ClientException("Job is not running, cannot shell into it")

        task_arn = job["container"]["taskArn"]
        job_queue_arn = job["jobQueue"]
        job_queue = self._batch_client.describe_job_queues(jobQueues=[job_queue_arn])[
            "jobQueues"
        ][0]

        # these are all the possible compute environments that the job could've been scheduled on
        possible_compute_environment_arns = [
            e["computeEnvironment"] for e in job_queue["computeEnvironmentOrder"]
        ]
        possible_compute_environments = (
            self._batch_client.describe_compute_environments(
                computeEnvironments=possible_compute_environment_arns,
            )["computeEnvironments"]
        )

        # these are all the possible ECS clusters (corresponding to AWS Batch compute environments) that
        # the job could be running in
        possible_ecs_cluster_arns = [
            e["ecsClusterArn"] for e in possible_compute_environments
        ]

        job_cluster_arn = None
        task = None
        for cluster_arn in possible_ecs_cluster_arns:
            tasks = self._ecs_client.describe_tasks(
                cluster=cluster_arn,
                tasks=[task_arn],
            )["tasks"]

            if len(tasks) == 0:
                continue

            job_cluster_arn = cluster_arn
            task = tasks[0]
            break

        if job_cluster_arn is None:
            raise ClientException(
                "Could not find the corresponding ECS cluster for the job"
            )

        container_arn = task["containerInstanceArn"]
        container_instance = self._ecs_client.describe_container_instances(
            containerInstances=[container_arn],
            cluster=job_cluster_arn,
        )["containerInstances"][0]

        ec2_instance_id = container_instance["ec2InstanceId"]

        instance = self._ec2_client.describe_instances(
            InstanceIds=[ec2_instance_id],
        )[
            "Reservations"
        ][0]["Instances"][0]

        network_interfaces = instance["NetworkInterfaces"]
        public_ip = None
        for interface in network_interfaces:
            if "Association" in interface:
                if "PublicDnsName" in interface["Association"]:
                    public_ip = interface["Association"]["PublicDnsName"]
                    break

        if public_ip is None:
            raise ClientException("Cannot find public IP address for instance")

        key = tempfile.mktemp()
        with open(key, "w") as f:
            f.write(self.config["ssh-key"])

        p = subprocess.Popen(
            [
                "ssh",
                "-vvv",
                "-i",
                key,
                f"ec2-user@{public_ip}",
                "docker",
                "ps",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate()
        rc = p.returncode

        if rc != 0:
            raise ClientException(f"Got error: \n{stderr.decode('utf-8')}")

        stdout = stdout.decode("utf-8")
        lines = stdout.splitlines()
        if lines[0].split()[0] != "CONTAINER":
            raise ClientException("Cannot find docker container")

        num_amazon_containers = 0
        non_amazon_containers = []
        for line in lines[1:]:
            if not line:
                continue
            parts = line.split(" ")
            parts = [p for p in parts if p]

            container_id = parts[0]
            image = parts[1]
            if image.startswith("amazon"):
                num_amazon_containers += 1
            else:
                non_amazon_containers.append(container_id)

        if num_amazon_containers == 0 or len(non_amazon_containers) != 1:
            raise ClientException("Cannot find docker container")

        container_id = non_amazon_containers[0]

        subprocess.call(
            [
                "ssh",
                "-t",
                "-i",
                key,
                "-o",
                "StrictHostKeyChecking=no",
                f"ec2-user@{public_ip}",
                f"docker exec -it {container_id} /bin/bash",
            ]
        )

        os.remove(key)

    def cancel(self, job_id: str):
        pass

    def delete(self, job_id: str):
        pass

    @staticmethod
    def supports_shell() -> bool:
        return True
