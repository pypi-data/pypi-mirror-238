from __future__ import annotations

import mknodes as mk


def test_virtual_files():
    nav = mk.MkNav()
    subnav = nav.add_nav("subsection")
    page = subnav.add_page("page")
    img = mk.MkBinaryImage(data=b"", path="Test.jpg")
    page.append(img)
