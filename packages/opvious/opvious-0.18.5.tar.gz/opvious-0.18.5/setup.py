# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opvious',
 'opvious.client',
 'opvious.data',
 'opvious.executors',
 'opvious.modeling',
 'opvious.specifications']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2,<3.0',
 'humanize>=4.4.0,<5.0.0',
 'importnb>=2023.1.7,<2024.0.0',
 'numpy>=1.21',
 'pandas>=1.4']

extras_require = \
{'aio': ['aiohttp>=3.8,<4.0', 'Brotli>=1.0.9,<2.0.0'],
 'cli': ['docopt>=0.6.2,<0.7.0']}

setup_kwargs = {
    'name': 'opvious',
    'version': '0.18.5',
    'description': 'Opvious Python SDK',
    'long_description': '# Opvious Python SDK  [![CI](https://github.com/opvious/sdk.py/actions/workflows/ci.yml/badge.svg)](https://github.com/opvious/sdk.py/actions/workflows/ci.yml) [![Pypi badge](https://badge.fury.io/py/opvious.svg)](https://pypi.python.org/pypi/opvious/)\n\n<div align="center">\n  <p>\n    Define and deploy optimization models in minutes with <a href="https://www.opvious.io">Opvious</a>. No solver installation required.\n  </p>\n  <a href="https://www.opvious.io/notebooks/retro/notebooks/?path=guides/welcome.ipynb"><img src="https://www.opvious.io/opvious-steps.png" style="height: 600px;"/></a>\n</div>\n\n\n## Highlights\n\n+ Declarative modeling API with __extensive static checks and automatic LaTeX generation__\n+ Remote solves with __real-time progress notifications__\n+ __Flexible data import/export__ via `pandas`\n+ __Advanced multi-objective support__: weighted sums, epsilon constraints, ...\n+ __Smart debugging capabilities__: semantic constraint relaxations, annotated LP formatting, ...\n\n\n## Documentation\n\n+ [Getting started guide](https://www.opvious.io/notebooks/retro/notebooks/?path=guides/welcome.ipynb)\n+ [SDK API reference](https://opvious.readthedocs.io)\n+ [Interactive optimization notebooks](https://github.com/opvious/notebooks)\n\n\n## Licensing\n\nThe SDK is licensed under Apache 2.0. The Opvious platform is available both as a managed cloud service (free on small datasets) and self-hosted (free for non-commercial projects). See our [plans page](https://www.opvious.io/plans) for more information.\n',
    'author': 'Opvious Engineering',
    'author_email': 'oss@opvious.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opvious/sdk.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
