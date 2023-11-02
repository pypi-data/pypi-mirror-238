
import os
from .config import CONFIG


def run_on_remote(file_path=None):
    ssh_command_base = "ssh -i {} {}".format(CONFIG["SSH_PRIVATE_KEY_PATH"], CONFIG["REMOTE_SERVER"])
    if CONFIG["GPU"] == True:
        docker_run_cmd = "sudo docker run --gpus all -v /home/ubuntu:/home {}/{}".format(CONFIG["DOCKER_REGISTRY"], CONFIG["DOCKER_IMAGE_NAME"])
    else:
        docker_run_cmd = "sudo docker run -v /home/ubuntu:/home {}/{}".format(CONFIG["DOCKER_REGISTRY"], CONFIG["DOCKER_IMAGE_NAME"])
    if file_path:
        docker_run_cmd += f" python {file_path}"
    commands = [
        "sudo docker pull {}/{}".format(CONFIG["DOCKER_REGISTRY"], CONFIG["DOCKER_IMAGE_NAME"]),
        docker_run_cmd
    ]
    for cmd in commands:
        os.system(f"{ssh_command_base} '{cmd}'")
def fetch_results(local_dir="./results"):
    os.system("scp -i {} -r {}:{}/results {}".format(CONFIG["SSH_PRIVATE_KEY_PATH"], CONFIG["REMOTE_SERVER"], CONFIG["REMOTE_WORKDIR"], local_dir))