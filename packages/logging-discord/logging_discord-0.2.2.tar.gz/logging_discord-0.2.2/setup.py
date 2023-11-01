# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging_discord']

package_data = \
{'': ['*']}

install_requires = \
['config>=0.5.1,<0.6.0', 'dynaconf>=3.2.3,<4.0.0', 'httpx>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'logging-discord',
    'version': '0.2.2',
    'description': 'The Logging Discord is a tool that simplifies the logging of error messages to a Discord channel. It allows you to send error messages with custom information, including a traceback and specific messages',
    'long_description': '<img src="https://logging-discord.readthedocs.io/en/latest/img/logging_discord.png" width="350">\n\n# Logging Discord\n[![Documentation Status](https://readthedocs.org/projects/logging-discord/badge/?version=latest)](https://logging-discord.readthedocs.io/en/latest/?badge=latest)\n[![CI](https://github.com/brunobrown/logging-discord/actions/workflows/pipeline.yml/badge.svg)](https://github.com/brunobrown/logging-discord/actions/workflows/pipeline.yml)\n[![codecov](https://codecov.io/gh/brunobrown/logging-discord/graph/badge.svg?token=XTB97RAJA6)](https://codecov.io/gh/brunobrown/logging-discord)\n\n- [English](README.md)\n- [Português](README-pt.md)\n\n`Logging Discord` is a tool that streamlines error message logging to a Discord channel. It enables the sending of tracebacks and custom specific information messages. Below, you will find details, parameters and methods, as well as usage examples.\n\n## Table of Contents\n\n- [How to Install the Package?](#how-to-install-the-package)\n- [How to Use the Package?](#how-to-use-the-package)\n- [Configuration via \'discord_config.py\'](#configuration-via-discord_configpy)\n- [Usage Examples](#usage-examples)\n- [Donations](#donations)\n\n## How to Install the Package?\n\n```bash\npip install logging_discord\n\n```\n\n## How to Use the Package?\n### Quick Start.\n\n```python\nfrom logging_discord import LogDiscord\n\nlog_discord = LogDiscord(webhook=\'https://your_discord_channel_webhook\')\n\nlog_discord.send(log_level=1)   # 0 = unknown, 1 = debug, 2 = info, 3 = warning, 4 = error, 5 = critical\n```\n\n<img src="https://logging-discord.readthedocs.io/en/latest/img/error_message.png">\n\n---\n\n## Configuration with `discord_config.py`\n\nYou can configure the parameters of the `LogDiscord` class by creating a file called \'discord_config.py\' at the root of the project. The \'discord_config.py\' file should contain the following configurations:\n\nExample:\n\n```python\nchannel = {\n    \'webhook\': \'https://discord.com/api/webhooks/example\',\n    \'avatar_url\': \'https://i0.wp.com/www.theterminatorfans.com/wp-content/uploads/2012/09/the-terminator3.jpg?resize=900%2C450&ssl=1\',\n    \'mode\': \'DEVELOPMENT\',\n    \'app_name\': \'APP_TEST\',\n}\n\nlog_levels = {\n    #   color legend:\n    #   * UNKNOWN: 0 = Black\n    #   * DEBUG: 35840 = Green\n    #   * INFO: 2196944 = Blue\n    #   * WARNING: 16497928 = Yellow\n    #   * ERROR: 16729344 = Red Orange\n    #   * CRITICAL: 12255250 = Red\n    \n    0: {\n        \'emoji\': \':thinking:   \',\n        \'title\': \'UNKNOWN\',\n        \'color\': 0,\n    },\n    1: {\'emoji\': \':beetle:   \', \'title\': \'DEBUG\', \'color\': 35840},\n    2: {\n        \'emoji\': \':information_source:   \',\n        \'title\': \'INFO\',\n        \'color\': 2196944,\n    },\n    3: {\n        \'emoji\': \':warning:   \',\n        \'title\': \'WARNING\',\n        \'color\': 16497928,\n    },\n    4: {\'emoji\': \':x:   \', \'title\': \'ERROR\', \'color\': 16729344},\n    5: {\'emoji\': \':sos:   \', \'title\': \'CRITICAL\', \'color\': 12255250},\n}\n```\n\n---\n\n## Usage Examples\n\nHere are some examples of how to use the `LogDiscord` class:\n\n```python\n# Creating a logger instance\nlogger = LogDiscord(webhook="your_webhook_url", avatar_url="avatar_url", mode="DEVELOPMENT", app_name="MyApp")\n\n# Sending an error log with traceback\nlogger.send(show_traceback=True, error_message="Critical error occurred!", log_level=5)\n\n# Sending an information log\nlogger.send(show_traceback=False, error_message="Operation successful.", log_level=2)\n```\n\n#### Remember to adjust the parameters according to your needs and customize error messages as necessary.\n\n---\n\n## Donations\n\nThank you for considering supporting the project! Your help is greatly appreciated and it enables me to continue developing and maintaining the software.\n\n[Support the Project](https://logging-discord.readthedocs.io/en/latest/#support-the-project)\n\n---\n\n<img src="https://logging-discord.readthedocs.io/en/latest/img/proverbs_16_3.jpg" width="500">\n\n[Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)\n\n',
    'author': 'bruno_brown',
    'author_email': 'brunobrown.86@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
