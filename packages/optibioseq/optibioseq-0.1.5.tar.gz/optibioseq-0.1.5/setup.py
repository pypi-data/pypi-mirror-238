# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['optibioseq']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'numpy>=1.22.2,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'optibioseq',
    'version': '0.1.5',
    'description': 'Program that helps wetlab members to analyze results from popular epitope prediction tools',
    'long_description': None,
    'author': 'Iván Corona Guerrero',
    'author_email': '<ivan.corona@uaq.mx>',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
