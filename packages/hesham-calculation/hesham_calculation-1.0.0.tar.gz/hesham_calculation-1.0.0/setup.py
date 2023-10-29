from setuptools import setup, find_packages

setup(
    name='hesham_calculation',
    packages=find_packages(where="app"),
    version='1.0.0',
    description='calculate some items',
    author='Hesham',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)