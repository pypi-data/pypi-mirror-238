"""Common templates used between pages in the app."""

from code import styles
from code.components.sidebar import sidebar
from code.state import State
from typing import Callable

import nextpy as xt

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


def menu_button() -> xt.Component:
    """The menu button on the top right of the page.

    Returns:
        The menu button component.
    """
    return xt.box(
        xt.menu(
            xt.menu_button(
                xt.icon(
                    tag="hamburger",
                    size="4em",
                    color=styles.text_color,
                ),
            ),
            xt.menu_list(
                xt.menu_item(xt.link("Home", href="/", width="100%")),
                xt.menu_divider(),
                xt.menu_item(
                    xt.link("About", href="https://github.com/dot-agent", width="100%")
                ),
                xt.menu_item(
                    xt.link("Contact", href="mailto:anurag@dotagent.ai", width="100%")
                ),
            ),
        ),
        position="fixed",
        right="1.5em",
        top="1.5em",
        z_index="500",
    )


def template(
    **page_kwargs: dict,
) -> Callable[[Callable[[], xt.Component]], xt.Component]:
    """The template for each page of the app.

    Args:
        page_kwargs: Keyword arguments to pass to the page.

    Returns:
        The template with the page content.
    """

    def decorator(page_content: Callable[[], xt.Component]) -> xt.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.
        """
        # Get the meta tags for the page.
        page_kwargs["meta"] = [*default_meta, *page_kwargs.get("meta", [])]

        @xt.page(**page_kwargs)
        def templated_page():
            return xt.hstack(
                sidebar(),
                xt.box(
                    xt.box(
                        page_content(),
                        **styles.template_content_style,
                    ),
                    **styles.template_page_style,
                ),
                xt.spacer(),
                menu_button(),
                align_items="flex-start",
                transition="left 0.5s, width 0.5s",
                position="relative",
                left=xt.cond(
                    State.sidebar_displayed, "0px", f"-{styles.sidebar_width}"
                ),
            )

        return templated_page

    return decorator
