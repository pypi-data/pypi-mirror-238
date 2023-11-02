
import os
from config import DOCKER_IMAGE_NAME, DOCKER_REGISTRY, USER_CODE_PATH

def build_image():
    # Dynamically generate Dockerfile
    with open("./Dockerfile", 'w') as f:
        f.write(f'''
FROM pytorch/pytorch:latest

WORKDIR /app

# Install Transformers
RUN pip install transformers

# Copy user's code and any necessary data
COPY {USER_CODE_PATH} /app/user_code.py

CMD ["python", "user_code.py"]
''')
    os.system(f"docker build -t {DOCKER_IMAGE_NAME} .")

def push_image():
    os.system(f"docker push {DOCKER_REGISTRY}/{DOCKER_IMAGE_NAME}")
