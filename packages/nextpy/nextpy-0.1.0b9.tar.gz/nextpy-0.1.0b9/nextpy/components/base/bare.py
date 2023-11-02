"""A bare component."""
from __future__ import annotations

from typing import Any

from nextpy.components.component import Component
from nextpy.components.tags import Tag
from nextpy.components.tags.tagless import Tagless
from nextpy.core.vars import Var


class Bare(Component):
    """A component with no tag."""

    contents: Var[str]

    @classmethod
    def create(cls, contents: Any) -> Component:
        """Create a Bare component, with no tag.

        Args:
            contents: The contents of the component.

        Returns:
            The component.
        """
        if isinstance(contents, Var) and contents._var_state:
            contents = contents.to(str)
        else:
            contents = str(contents)
        return cls(contents=contents)  # type: ignore

    def _render(self) -> Tag:
        return Tagless(contents=str(self.contents))
