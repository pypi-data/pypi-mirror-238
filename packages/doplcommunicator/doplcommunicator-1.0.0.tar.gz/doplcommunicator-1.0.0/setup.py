from setuptools import find_packages, setup

setup(
    name='doplcommunicator',
    packages=find_packages(include=['doplcommunicator']),
    version='1.0.0',
    description='Communicates data between dopl and devices',
    author='Ryan James, PhD',
    install_requires=['python-socketio', "requests"],
)