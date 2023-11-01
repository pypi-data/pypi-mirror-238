# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openbb_ultima', 'openbb_ultima.models', 'openbb_ultima.utils']

package_data = \
{'': ['*']}

install_requires = \
['openbb-core>=0.1.0a2,<0.2.0']

entry_points = \
{'openbb_provider_extension': ['ultima = openbb_ultima:ultima_provider']}

setup_kwargs = {
    'name': 'openbb-ultima',
    'version': '0.1.0a4',
    'description': 'Ultima Insights extension for OpenBB',
    'long_description': '# OpenBB Ultima Provider\n\nThis extension integrates the [Ultima Insights](https://www.ultimainsights.ai/) data provider into the OpenBB Platform.\n\n## Installation\n\nTo install the extension:\n\n```bash\npip install openbb-ultima\n```\n\nFor development please check [Contribution Guidelines](https://github.com/OpenBB-finance/OpenBBTerminal/blob/feature/openbb-sdk-v4/openbb_platform/CONTRIBUTING.md).\n\nDocumentation available [here](https://docs.openbb.co/sdk).\n',
    'author': 'Ultima Insights Team',
    'author_email': 'hello@ultimainsights.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
