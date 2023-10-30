# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anymail_history', 'anymail_history.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-anymail>=9.0', 'django>=3.2']

setup_kwargs = {
    'name': 'anymail-history',
    'version': '0.1.8',
    'description': 'Email History for Django Anymail',
    'long_description': '# anymail-history - Email History (database storage) for [Django Anymail](https://anymail.dev/)\n\n[![CI tests](https://github.com/pfouque/django-anymail-history/actions/workflows/test.yml/badge.svg)](https://github.com/pfouque/django-anymail-history/actions/workflows/test.yml)\n[![codecov](https://codecov.io/github/pfouque/django-anymail-history/branch/master/graph/badge.svg?token=GWGDR6AR6D)](https://codecov.io/github/pfouque/django-anymail-history)\n[![Documentation](https://img.shields.io/static/v1?label=Docs&message=READ&color=informational&style=plastic)](https://github.com/pfouque/django-anymail-history#settings)\n[![MIT License](https://img.shields.io/static/v1?label=License&message=MIT&color=informational&style=plastic)](https://github.com/pfouque/anymail-history/LICENSE)\n\nKeep history of all emails sent by [Django Anymail](https://anymail.dev/)\n\n## Introduction\n\nanymail-history implements database storage for Django Anymail.\n\n## Resources\n\n-   Package on PyPI: [https://pypi.org/project/anymail-history/](https://pypi.org/project/anymail-history/)\n-   Project on Github: [https://github.com/pfouque/django-anymail-history](https://github.com/pfouque/django-anymail-history)\n\n## Features\n\n-   Store sent emails\n-   Store tracking events\n-   Display Admin\n-   html templating ?\n\n\n## Requirements\n\n-   Django >=3.2\n-   Python >=3.8\n\n## How to\n\n1. [Install Anymail](https://anymail.dev/en/stable/quickstart/)\n\n2. Install\n    ```\n    $ pip install "django-anymail-history"\n    ```\n\n3. Register anymail_history in your list of Django applications:\n    ```\n    INSTALLED_APPS = [\n        # ...\n        "anymail",\n        "anymail_history",\n        # ...\n    ]\n    ```\n4. Then migrate the app to create the database table\n    ```manage.py migrate```\n\n5. 🎉 Voila!\n\n## Settings\n\nYou can add settings to your project’s settings.py either as a single `ANYMAIL` dict, or by breaking out individual settings prefixed with ANYMAIL_. So this settings dict:\n\n```\nANYMAIL = {\n    "STORE_HTML": True,\n}\n```\n…is equivalent to these individual settings:\n\n```\nANYMAIL_STORE_HTML = True\n```\n\n### Available settings\n\n-   `ANYMAIL_STORE_FAILED_SEND`: (default: False) Store message even if esp didn\'t returned a message-id.\n-   `ANYMAIL_STORE_HTML`: (default: False) Store html alternatives.\n\n## Contribute\n\n### Principles\n\n-   Simple for developers to get up-and-running\n-   Consistent style (`black`, `ruff`)\n-   Future-proof (`pyupgrade`)\n-   Full type hinting (`mypy`)\n\n### Coding style\n\nWe use [pre-commit](https://pre-commit.com/) to run code quality tools.\n[Install pre-commit](https://pre-commit.com/#install) however you like (e.g.\n`pip install pre-commit` with your system python) then set up pre-commit to run every time you\ncommit with:\n\n```bash\n> pre-commit install\n```\n\nYou can then run all tools:\n\n```bash\n> pre-commit run --all-files\n```\n\nIt includes the following:\n\n-   `poetry` for dependency management\n-   `Ruff`, `black` and `pyupgrade` linting\n-   `mypy` for type checking\n-   `Github Actions` for builds and CI\n\nThere are default config files for the linting and mypy.\n\n### Tests\n\n#### Tests package\n\nThe package tests themselves are _outside_ of the main library code, in a package that is itself a\nDjango app (it contains `models`, `settings`, and any other artifacts required to run the tests\n(e.g. `urls`).) Where appropriate, this test app may be runnable as a Django project - so that\ndevelopers can spin up the test app and see what admin screens look like, test migrations, etc.\n\n#### Running tests\n\nThe tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment,\nyou can run them thus:\n\n```\n$ poetry run pytest\n```\n\nor\n\n```\n$ poetry shell\n(anymail-history-py3.10) $ pytest\n```\n\n#### CI\n\n- `.github/workflows/lint.yml`: defines and ensure coding rules on Github.\n\n- `.github/workflows/test.yml`: Runs tests on all compatible combinations of Django (3.2+) & Anymail(8.4+), Python (3.8+)in a Github matrix.\n\n- `.github/workflows/coverage.yml`: Calculates the coverage on an up to date version.\n',
    'author': 'Pascal Fouque',
    'author_email': 'fouquepascal@gmail.com',
    'maintainer': 'Pascal Fouque',
    'maintainer_email': 'fouquepascal@gmail.com',
    'url': 'https://github.com/pfouque/anymail-history',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
