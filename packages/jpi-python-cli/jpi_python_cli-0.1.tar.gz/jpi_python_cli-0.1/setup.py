from setuptools import setup, find_packages

setup(
    name='jpi_python_cli',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jpi_python_cli = src.main:main',
        ],
    },
)