import json
import os
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

import click
from loguru import logger

import komodo_cli.printing as printing

SUPPORTED_COMPUTE_SERVICES = ["eks"]


def run_cmd(cmd, print_stdout=True) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )

    if print_stdout:
        for line in iter(proc.stdout.readline, ""):
            click.echo(line)

    stdout, stderr = proc.communicate()
    exit_code = proc.returncode

    return exit_code, stdout, stderr


def get_compute_dir() -> str:
    komo_dir = os.environ.get(
        "KOMODO_DIR",
        os.path.join(os.path.expanduser("~"), ".komo"),
    )

    compute_dir = os.path.join(komo_dir, "compute")
    return compute_dir


def get_vars_filepath() -> str:
    return os.path.join(get_compute_dir(), "komodo.tfvars")


def print_clusters():
    cmd = [
        "terraform",
        f"-chdir={get_compute_dir()}",
        "output",
        "-json",
        "|",
        "jq",
    ]
    exit_code, stdout, stderr = run_cmd(" ".join(cmd), print_stdout=False)
    if exit_code != 0:
        logger.error(stderr)
        printing.error("Error listing compute", bold=True)
        sys.exit(1)

    outputs = json.loads(stdout.strip())
    clusters = defaultdict(dict)
    for k, v in outputs.items():
        s = k.split("_")
        cluster_type = s[0]
        var = "_".join(s[2:])
        clusters[cluster_type][var] = v

    for cluster_type, cluster_values in clusters.items():
        click.echo(
            f"{click.style(cluster_type, bold=True)} - {click.style(cluster_values['id']['value'], fg='green', bold=True)}"
        )
        cluster_values.pop("id")
        for k, v in cluster_values.items():
            click.echo(f"{click.style(k, fg='yellow')}: {v['value']}")


def dict_to_txt_file(d: Dict, output_path: str):
    with open(output_path, "w") as file:
        for k, v in d.items():
            if isinstance(v, list) or isinstance(v, dict):
                v = json.dumps(v).replace(":", "=")
            else:
                if not v.startswith('"') and not v.endswith('"'):
                    v = f'"{v}"'

            file.write(f"{k} = {v}\n")


def txt_to_dict(input_path: str) -> Dict:
    output = {}
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                v = v.replace("=", ":")

                if v.startswith("[") and v.endswith("]"):
                    v = json.loads(v)
                if v.startswith("{") and v.endswith("}"):
                    v = json.loads(v)

                output[k] = v
    return output


def get_vars(no_exist_ok=False):
    compute_dir = get_compute_dir()
    vars_path = os.path.join(compute_dir, "komodo.tfvars")

    if not os.path.exists(vars_path):
        if no_exist_ok:
            return {}
        raise FileNotFoundError(f"Variables file not found at {vars_path}")
    else:
        return txt_to_dict(vars_path)


def update_vars(new_vars: Dict):
    compute_dir = get_compute_dir()
    vars_path = os.path.join(compute_dir, "komodo.tfvars")
    dict_to_txt_file(new_vars, vars_path)
