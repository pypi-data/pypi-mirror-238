
import os
from config import DOCKER_IMAGE_NAME, DOCKER_REGISTRY, REMOTE_SERVER, REMOTE_WORKDIR, SSH_PRIVATE_KEY_PATH

def run_on_remote():
    ssh_command_base = f"ssh -i {SSH_PRIVATE_KEY_PATH} {REMOTE_SERVER}"
    commands = [
        f"docker pull {DOCKER_REGISTRY}/{DOCKER_IMAGE_NAME}",
        f"docker run --gpus all {DOCKER_REGISTRY}/{DOCKER_IMAGE_NAME}"
    ]
    for cmd in commands:
        os.system(f"{ssh_command_base} '{cmd}'")

def fetch_results(local_dir="./results"):
    os.system(f"scp -i {SSH_PRIVATE_KEY_PATH} -r {REMOTE_SERVER}:{REMOTE_WORKDIR}/results {local_dir}")
