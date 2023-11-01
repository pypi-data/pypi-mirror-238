# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brickworks',
 'brickworks.auth',
 'brickworks.auth.routes',
 'brickworks.cli',
 'brickworks.db',
 'brickworks.migration',
 'brickworks.object',
 'brickworks.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.19.0,<0.20.0',
 'alembic>=1.12.0,<2.0.0',
 'fastapi>=0.104.0,<0.105.0',
 'httpx>=0.25.0,<0.26.0',
 'pydantic-settings>=2.0.3,<3.0.0',
 'sqlalchemy>=2.0.22,<3.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['mason = brickworks.cli:main']}

setup_kwargs = {
    'name': 'brickworks',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'jens',
    'author_email': 'jens.kuerten42@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
