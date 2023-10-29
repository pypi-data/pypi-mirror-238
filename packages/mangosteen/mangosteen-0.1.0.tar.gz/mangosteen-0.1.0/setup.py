# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mangosteen']

package_data = \
{'': ['*'], 'mangosteen': ['static/zcss/*', 'static/zjs/*', 'static/zwc/*']}

install_requires = \
['json-cfg', 'pymongo']

setup_kwargs = {
    'name': 'mangosteen',
    'version': '0.1.0',
    'description': 'Web widgets',
    'long_description': 'Web widgets for python',
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
