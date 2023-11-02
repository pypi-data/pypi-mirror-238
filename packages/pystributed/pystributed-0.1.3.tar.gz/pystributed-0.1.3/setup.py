
from setuptools import setup, find_packages

setup(
    name='pystributed',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[],
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility to run Jupyter Notebook code on a remote server using Docker.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pystributed',
)
