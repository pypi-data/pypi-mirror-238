
from setuptools import setup, find_packages

setup(
    name='pystributed',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],
    author='Evan Anthony',
    author_email='anthonyevanm@gmail.com',
    description='A utility to run Jupyter Notebook code on a remote server using Docker.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eanthony76/pystributed',
)
