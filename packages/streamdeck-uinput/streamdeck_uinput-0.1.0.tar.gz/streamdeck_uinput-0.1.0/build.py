from typing import Any, Dict

from setuptools import Extension

ext_modules = [
    Extension(
        "streamdeck_uinput._uinput", ["streamdeck_uinput/uinput.c"],
    ),
]


def build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
        }
    )