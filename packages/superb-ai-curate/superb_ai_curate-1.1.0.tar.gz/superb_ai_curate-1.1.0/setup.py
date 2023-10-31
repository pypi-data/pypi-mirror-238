# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spb_curate',
 'spb_curate.abstract',
 'spb_curate.abstract.api',
 'spb_curate.curate',
 'spb_curate.curate.api',
 'spb_curate.curate.model']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

extras_require = \
{'dev': ['black', 'coveralls', 'isort', 'pytest', 'pytest-cov'],
 'docs': ['Sphinx',
          'sphinxcontrib-napoleon',
          'sphinx-autodoc-typehints>=1.19.4,<2.0.0',
          'sphinx-pyproject',
          'sphinx-rtd-theme']}

setup_kwargs = {
    'name': 'superb-ai-curate',
    'version': '1.1.0',
    'description': 'The official Superb AI Curate client for Python',
    'long_description': '# `superb-ai-curate`\n\n[![Coverage Status](https://coveralls.io/repos/github/Superb-AI-Suite/superb-ai-curate-python/badge.svg?branch=main)](https://coveralls.io/github/Superb-AI-Suite/superb-ai-curate-python?branch=main)\n[![Version](https://img.shields.io/pypi/v/superb-ai-curate)](https://pypi.org/project/superb-ai-curate/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)\n\n## Overview\n\n`superb-ai-curate` is the Python client for interacting with [Superb Curate](https://superb-ai.com/).\n\n## Installation\n\nYou don\'t need this source code unless you want to modify the package. If you just want to use the package, just run:\n\n```bash\n$ pip install --upgrade superb-ai-curate\n```\n\n### Requirements\n\nPython 3.7+\n\n## Documentation\n\nYou can also find the documentation for `superb-ai-curate` [on the website](https://superb-ai-curate-python.readthedocs.io/en/latest/).\n\n* [Introduction](https://superb-ai-curate-python.readthedocs.io/en/latest/intro/overview.html)\n* [Installation](https://superb-ai-curate-python.readthedocs.io/en/latest/intro/install.html)\n* [Tutorial](https://superb-ai-curate-python.readthedocs.io/en/latest/intro/tutorial.html)\n\n## Usage\n\nAn Access Key is required to use the python client. This can be generated from the Settings > Access menu on the Superb AI Curate website. For more details on access key issuance and management, you can check the [Access Key Management](https://docs.superb-ai.com/reference/access-key-management) documentation. The Team Name refers to the organization name that your personal account belongs to.\n\n```python\nimport spb_curate\nfrom spb_curate import curate\n\nspb_curate.access_key = "..."\nspb_curate.team_name = "..."\n\ndataset = curate.fetch_dataset(id="...")\n\nimages = [\n    curate.Image(\n        key="<unique image key>",\n        source=curate.ImageSourceLocal(asset="/path/to/image"),\n        metadata={"weather": "clear", "timeofday": "daytime"},\n    ),\n    curate.Image(\n        key="<unique image key>",\n        source=curate.ImageSourceLocal(asset="/path/to/image"),\n        metadata={"weather": "clear", "timeofday": "daytime"},\n    ),\n]\n\njob: curate.Job = dataset.add_images(images=images)\njob.wait_until_complete()\n\n```\n\n### Configuring per-request\n\nFor use with multiple credentials, the requests can be configured at the function level.\n\n```python\nfrom spb_curate import curate\n\ndataset = curate.fetch_dataset(access_key="...", team_name="...", id="...")\n```\n\n### Logging\n\nIf required, the client can be configured to produce basic logging output. There are two levels that are logged to, `INFO` and `DEBUG`. For production use, `INFO` is the recommended logging level, however `DEBUG` can be used for more verbosity.\n\nThere are several methods for setting the log level.\n\n1. Environment variable\n\n```bash\n$ export SPB_LOG_LEVEL = "INFO"\n```\n\n2. Superb AI Curate Python client global setting\n\n```python\nimport spb_curate\n\nspb_curate.log_level = "INFO"\n```\n\n3. Python logging library\n\n```python\nimport logging\n\nlogging.basicConfig()\nlogging.getLogger("superb-ai").setLevel(logging.INFO)\n```\n\n### Development\n\nThe development environment relies on [Poetry](https://python-poetry.org/) for package management, testing and building.\n\n```bash\n$ poetry install -E dev\n$ poetry run pytest --cov=spb_curate tests\n```\n',
    'author': 'Superb AI',
    'author_email': 'support@superb-ai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://superb-ai.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
