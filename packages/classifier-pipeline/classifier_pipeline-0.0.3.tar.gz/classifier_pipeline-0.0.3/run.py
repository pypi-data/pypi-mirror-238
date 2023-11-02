#!/usr/bin/env python3

import argparse
import os
import subprocess
import getpass

IMAGE_NAME = "pipeline-train"
CONTAINER_NAME = "pipeline-train"


print("Stopping {} container (if running)".format(CONTAINER_NAME))
remove_container_cmd = ["docker", "rm", "--force", CONTAINER_NAME]
subprocess.call(
    add_sudo(remove_container_cmd), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
)

print("Building container")
build_container_cmd = ["docker", "build", ".", "-t", IMAGE_NAME]
subprocess.check_call(add_sudo(build_container_cmd))


print("Starting container")
print("volume is " + os.getcwd())
base_path = os.path.dirname(os.getcwd())
run_cmd = [
    "docker",
    "run",
    "-td",
    "--rm",
    "--name",
    CONTAINER_NAME,
    "--volume",
    "/home/cp/cacophony/classifier-pipeline" + ":/classifier-pipeline",
    "--volume",
    "/data" + ":/data",
]


run_cmd.append(IMAGE_NAME)
subprocess.check_call(add_sudo(run_cmd))
