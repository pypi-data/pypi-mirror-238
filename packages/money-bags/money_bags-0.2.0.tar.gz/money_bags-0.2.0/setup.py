# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['money_bags',
 'money_bags.constants',
 'money_bags.country_specifics',
 'money_bags.money_identifier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'money-bags',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.9.18',
}


setup(**setup_kwargs)
