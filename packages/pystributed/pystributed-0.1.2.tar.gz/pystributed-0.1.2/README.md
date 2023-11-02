
# PyStributed: Remote Execution Utility

This package allows users to mark specific code cells in a Jupyter Notebook for remote execution. Once marked, the code will be packaged into a Docker container, sent to a specified remote server for execution, and the results will be fetched back to the local machine.

## Installation

1. Extract the contents of `pystributed.zip` to a location on your machine.
2. Navigate to the directory and run `pip install .` to install the package.

## Prerequisites

- Docker installed on both local and remote machines.
- SSH access to the remote machine.
- PyTorch and Transformers libraries if you are using them in your code.

## Configuration

Before using the package, you need to set up some configurations in `config.py`:

- `DOCKER_IMAGE_NAME`: Name of the Docker image that will be created.
- `DOCKER_REGISTRY`: Docker registry where the image will be pushed.
- `REMOTE_SERVER`: SSH-compatible address of your remote server (e.g., `user@remote_server_ip`).
- `REMOTE_WORKDIR`: Working directory on the remote server where results will be stored.
- `USER_CODE_PATH`: Temporary path on the local machine where the user's code will be saved before packaging.

## Usage

1. In your Jupyter Notebook, import the package:

```python
import pystributed.main as runner
```

2. Use the `%%save_for_remote` magic command to mark the code cell you want to run remotely:

```python
%%save_for_remote

# Your code here
# For example:
import torch
model = torch.load('my_model.pth')
result = model(some_data)
```

3. After marking the desired code cell, call the main function from the package to execute the process:

```python
runner.main()
```

## Under the Hood

The package works in the following sequence:

1. The code cell marked with `%%save_for_remote` is saved to a Python script (`user_code.py` by default).
2. A Docker image is built with the user's code and necessary dependencies.
3. The Docker image is pushed to the specified Docker registry.
4. The package SSHs into the specified remote server, pulls the Docker image, and runs it.
5. Once the code execution is complete on the remote server, the results are fetched and saved to the local machine.
