# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neutrapy', 'neutrapy.commands']

package_data = \
{'': ['*'], 'neutrapy': ['data/*']}

install_requires = \
['cmdy>=0.5.0,<0.6.0', 'pyparam>=0.5.3,<0.6.0', 'rtoml>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['neutrapy = neutrapy.__main__:main']}

setup_kwargs = {
    'name': 'neutrapy',
    'version': '0.0.0',
    'description': 'Command line tool for build a desktop app using neutralinojs and python',
    'long_description': None,
    'author': 'pwwang',
    'author_email': '1188067+pwwang@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
