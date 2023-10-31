# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golem',
 'golem.cli',
 'golem.event_bus',
 'golem.event_bus.in_memory',
 'golem.managers',
 'golem.managers.activity',
 'golem.managers.agreement',
 'golem.managers.demand',
 'golem.managers.network',
 'golem.managers.payment',
 'golem.managers.proposal',
 'golem.managers.proposal.plugins',
 'golem.managers.proposal.plugins.negotiating',
 'golem.managers.proposal.plugins.scoring',
 'golem.managers.work',
 'golem.node',
 'golem.payload',
 'golem.payload.parsers',
 'golem.payload.parsers.textx',
 'golem.pipeline',
 'golem.resources',
 'golem.resources.activity',
 'golem.resources.agreement',
 'golem.resources.allocation',
 'golem.resources.debit_note',
 'golem.resources.demand',
 'golem.resources.invoice',
 'golem.resources.network',
 'golem.resources.pooling_batch',
 'golem.resources.proposal',
 'golem.utils',
 'golem.utils.low',
 'golem.utils.storage',
 'golem.utils.storage.gftp']

package_data = \
{'': ['*']}

install_requires = \
['async-exit-stack==1.0.1',
 'click>=8.1.3,<9.0.0',
 'jsonrpc-base>=1.0.3,<2.0.0',
 'prettytable>=3.4.1,<4.0.0',
 'semantic-version>=2.8,<3.0',
 'setuptools',
 'srvresolver>=0.3.5,<0.4.0',
 'textx>=3.1.1,<4.0.0',
 'ya-aioclient>=0.6.4,<0.7.0']

setup_kwargs = {
    'name': 'golem-core',
    'version': '0.2.0',
    'description': 'Golem Network (https://golem.network/) API for Python',
    'long_description': 'None',
    'author': 'Golem Factory',
    'author_email': 'contact@golem.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/golemfactory/golem-core-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
