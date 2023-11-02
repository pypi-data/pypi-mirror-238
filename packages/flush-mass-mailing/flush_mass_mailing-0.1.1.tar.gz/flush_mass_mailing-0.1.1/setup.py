from setuptools import setup, find_packages

setup(
    name='flush_mass_mailing',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'rich',
        'csv',
        'getpass',
        'time',
    ],
)