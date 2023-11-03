# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compose',
 'compose.command',
 'compose.dependency',
 'compose.event',
 'compose.messaging',
 'compose.messaging.queue',
 'compose.query',
 'compose.query.mongo',
 'compose.query.mongo.op',
 'compose.query.mongo.op.aggregation',
 'compose.repository',
 'compose.schema',
 'compose.types',
 'compose.v1',
 'compose.v1.command',
 'compose.v1.event',
 'compose.v1.query',
 'compose.v1.query.mongo',
 'compose.v1.query.mongo.op',
 'compose.v1.repository',
 'compose.v1.schema',
 'compose.v1.types']

package_data = \
{'': ['*']}

install_requires = \
['dependency-injector>=4.41.0,<5.0.0',
 'inflection>=0.5.1,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.0,<3',
 'pymongo[aws]>=4.3.3,<5.0.0']

extras_require = \
{'aws': ['boto3>=1.28.73,<2.0.0']}

setup_kwargs = {
    'name': 'pozalabs-compose',
    'version': '0.18.1',
    'description': 'Backend components for POZAlabs',
    'long_description': 'None',
    'author': 'sunwoong',
    'author_email': 'sunwoong@pozalabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
