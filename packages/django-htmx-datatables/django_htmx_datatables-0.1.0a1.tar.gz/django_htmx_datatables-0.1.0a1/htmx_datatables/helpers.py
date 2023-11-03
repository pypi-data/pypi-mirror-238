"""Helpers for htmx_datatables."""

import re
from enum import Enum


def add_enum_to_context(enum_class: Enum, context: dict):
    """Add enum to a request context."""
    enum_dict = {o.name: o.value for o in enum_class}
    context[enum_class.__name__] = enum_dict


def camel_to_snake(name: str, delimiter: str = "_") -> str:
    """Transform string in camel case to snake case. Delimiter can be configured."""
    replace_regex = r"\1" + delimiter + r"\2"
    name = re.sub(r"(.)([A-Z][a-z]+)", replace_regex, name)
    return re.sub(r"([a-z0-9])([A-Z])", replace_regex, name).lower()
