# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc2gd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mc2gd',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'itch',
    'author_email': 'marine.taichi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
