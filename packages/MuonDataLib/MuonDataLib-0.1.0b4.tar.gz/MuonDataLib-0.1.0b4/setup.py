from setuptools import find_packages, setup
from tools.setup_helper import get_extensions


VERSION = "0.1.0b4"
PACKAGE_NAME = 'MuonDataLib'


extensions = get_extensions(PACKAGE_NAME)

setup(
        name=PACKAGE_NAME,
        requires=['numpy'],
        setup_requires=['numpy>=1.12'],
        install_requires=['numpy>=1.12'],
        packages=find_packages(where='src'),
        description='A package for MuSR data',
        long_description='This package provides code for reading '
                         'and analysing data from MuSR experiments. ',
        author='Anthony Lim',
        ext_modules=extensions,
        author_email="anthony.lim@stfc.ac.uk",
        version=VERSION,
        license='BSD',
        package_dir={'': 'src'}
        )
