import setuptools

setuptools.setup(name='clfill', packages=['clfill'])

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='clfill',
    version='1.0.0',
    author='lorimv',
    description='uses docs api to fill my cover letter',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clfill = clfill.cli:main'
        ]
    },
    install_requires=install_requires,
)