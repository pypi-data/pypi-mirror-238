"""The home page of the app."""

from code import styles
from code.templates import template

import nextpy as xt


@template(route="/", title="Home", image="/logo.svg")
def index() -> xt.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md") as readme:
        content = readme.read()
    return xt.markdown(content, component_map=styles.markdown_style)
