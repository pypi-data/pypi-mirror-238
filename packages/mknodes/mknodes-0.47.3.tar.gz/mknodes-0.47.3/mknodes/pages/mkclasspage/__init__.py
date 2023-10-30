from __future__ import annotations

import os
import pathlib

from typing import Any

from mknodes.info import grifferegistry
from mknodes.pages import mktemplatepage
from mknodes.utils import classhelpers, log, reprhelpers


logger = log.get_logger(__name__)


DEFAULT_TPL = "classpage.md"


class MkClassPage(mktemplatepage.MkTemplatePage):
    """Page showing information about a class."""

    def __init__(
        self,
        klass: type,
        *,
        path: str | os.PathLike | None = None,
        module_path: tuple[str, ...] | str | None = None,
        template: str | os.PathLike | None = None,
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            klass: class to show info for
            module_path: If given, overrides module returned by class.__module__
                         This can be useful if you want to link to an aliased class
                         (for example a class imported to __init__.py)
            template: Name of the template to load
            path: Filename/path for the class page. defaults to [classname].md
            kwargs: keyword arguments passed to base class
        """
        self.klass = klass
        self.module_path = module_path
        # if user chooses custom template, we make default the parent
        tpl = template or DEFAULT_TPL
        super().__init__(
            path=path or pathlib.Path(f"{klass.__name__}.md"),
            template=tpl,
            template_parent=DEFAULT_TPL if tpl != DEFAULT_TPL else None,
            **kwargs,
        )

    @property
    def parts(self) -> tuple[str, ...]:
        match self.module_path:
            case None:
                return tuple(self.klass.__module__.split("."))
            case _:
                return classhelpers.to_module_parts(self.module_path)

    def __repr__(self):
        return reprhelpers.get_nondefault_repr(self)

    @property
    def extra_variables(self) -> dict[str, Any]:
        # right now, we inject the cls and the griffe Class into jinja namespace.
        subclasses = list(classhelpers.iter_subclasses(self.klass, recursive=False))
        variables = dict(cls=self.klass, subclasses=subclasses)
        variables["griffe_obj"] = grifferegistry.registry.get_class(self.klass)
        return variables


if __name__ == "__main__":
    import mknodes as mk

    doc = MkClassPage.with_context(mk.Environment)
    print(doc.to_markdown())
