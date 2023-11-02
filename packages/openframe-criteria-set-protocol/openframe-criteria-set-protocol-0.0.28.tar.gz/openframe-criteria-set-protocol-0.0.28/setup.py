from setuptools import find_packages, setup

setup(
    name='openframe_criteria_set_protocol',
    packages=find_packages(),
    version='0.0.28',
    description='A protocol and tools for defining and working with criteria sets',
    author='Andrés Angulo <aa@openframe.org>',
    install_requires=['marshmallow'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.2'],
    test_suite='tests'
)
