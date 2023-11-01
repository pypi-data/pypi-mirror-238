# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ni_measurementlink_generator']

package_data = \
{'': ['*'], 'ni_measurementlink_generator': ['templates/*']}

install_requires = \
['Mako>=1.2.1,<2.0.0', 'click>=8.1.3']

entry_points = \
{'console_scripts': ['ni-measurementlink-generator = '
                     'ni_measurementlink_generator.template:create_measurement']}

setup_kwargs = {
    'name': 'ni-measurementlink-generator',
    'version': '1.3.0.dev0',
    'description': 'MeasurementLink Code Generator for Python',
    'long_description': '# MeasurementLink™ Code Generator for Python\n\n---\n\n## Introduction\n\nMeasurementLink Code Generator for Python (`ni-measurementlink-generator`) is a\ntool for generating reusable measurement plug-ins using gRPC services.\n\nFor installation and usage, see [MeasurementLink Support for Python (`ni-measurementlink-service`)](https://pypi.org/project/ni-measurementlink-service/).\n\n---\n\n## Dependencies\n\n- Python >= 3.8 [(3.9 recommended)](https://www.python.org/downloads/release/python-3913/)\n- [mako >= 1.2.1, < 2.x](https://pypi.org/project/Mako/1.2.1/)\n- [click >= 8.1.3](https://pypi.org/project/click/8.1.3/)\n\n---',
    'author': 'NI',
    'author_email': 'opensource@ni.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ni/measurementlink-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
