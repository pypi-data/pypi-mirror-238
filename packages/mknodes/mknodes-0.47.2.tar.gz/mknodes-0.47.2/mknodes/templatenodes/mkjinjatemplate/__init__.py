from __future__ import annotations

from typing import Any

from mknodes.basenodes import mkcontainer
from mknodes.utils import log, reprhelpers


logger = log.get_logger(__name__)


class MkJinjaTemplate(mkcontainer.MkContainer):
    """Node representing a jinja template.

    Renders templates with the context-aware MkNodes jinja environment.
    Rendered nodes become virtual children of this node.
    Additional variables can be passed to the render process.
    """

    ICON = "simple/jinja"
    STATUS = "new"

    def __init__(
        self,
        template: str,
        *,
        variables: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            template: Jinja template name.
            variables: Variables to use for rendering
            kwargs: Keyword arguments passed to parent
        """
        super().__init__(**kwargs)
        self.template = template
        self.variables = variables or {}

    def __repr__(self):
        return reprhelpers.get_nondefault_repr(self)

    @property
    def items(self):
        self.env.render_template(self.template, variables=self.variables)
        return self.env.rendered_nodes

    @items.setter
    def items(self, val):
        pass

    @classmethod
    def create_example_page(cls, page):
        page += MkJinjaTemplate(template="nodes_index.jinja")

    def _to_markdown(self) -> str:
        return self.env.render_template(self.template, variables=self.variables)


if __name__ == "__main__":
    node = MkJinjaTemplate("nodes_index.jinja")
    print(node.get_resources())
