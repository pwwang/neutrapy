# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neutrapy',
 'neutrapy.commands',
 'neutrapy.templates.default.extensions',
 'neutrapy.templates.default.extensions.python']

package_data = \
{'': ['*'],
 'neutrapy': ['templates/default/*',
              'templates/default/resources/*',
              'templates/default/resources/js/*']}

install_requires = \
['pyparam>=0.5.3,<0.6.0', 'rtoml>=0.8.0,<0.9.0']

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
from building import *
build(setup_kwargs)

setup(**setup_kwargs)
