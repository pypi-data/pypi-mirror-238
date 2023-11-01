from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.1.4'
DESCRIPTION = 'Peptide prediction results analysis'
LONG_DESCRIPTION = 'A package that allows wetlab personel to easily analyse results from popular epitope prediction servers.'
install_requires = \
['bs4>=0.0.1,<0.0.2',
 'numpy>=1.22.2,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.0,<2.0.0']

# Setting up
setup(
    name="optibioseq",
    version=VERSION,
    author="Kamen Rider Ice (Iván Corona Guerrero), Dr. Francisco Solis Munoz",
    author_email="<ivan.corona@uaq.mx>, <siscomagma@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'Peptide', 'bioinformatics', 'forbidden arts'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
