# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamdeck_uinput']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'streamdeck_uinput',
    'version': '0.1.0',
    'description': 'Basic implementation of UInput for the Elgato Stream Deck',
    'long_description': '# UInput Python 3.11\nthis is a simple implementation of the UInput API for Linux in Python 3.11 compatible with Wayland and X11.\nfor kernel 5.11 and above. you need to enable the `uinput` module with `sudo modprobe uinput`.\n\nthis implementation is compatible with the UInput class of the `python-uinput` package. is made while the\nwayland support is fixed in the `python-uinput` package.# streamdeck_uinput\n',
    'author': 'Julian reyes Escrigas',
    'author_email': 'julian.reyes.escrigas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
