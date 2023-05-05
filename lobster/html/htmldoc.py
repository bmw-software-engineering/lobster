#!/usr/bin/env python3
#
# lobster_html_report - Visualise LOBSTER report in HTML
# Copyright (C) 2022 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import html

from lobster.html import assets

NAVBAR_STICKY_SCRIPT = """
window.onscroll = function() {stickyNavbar()};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function stickyNavbar() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}
"""


class Menu_Item:
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name

    def generate(self, doc):
        assert isinstance(doc, Document)
        assert False


class Menu_Link(Menu_Item):
    def __init__(self, name, target):
        assert isinstance(target, str)
        super().__init__(name)

        self.target = target

    def generate(self, doc):
        assert isinstance(doc, Document)
        rv = '<a href="%s">' % self.target
        if self.target.startswith("http"):
            rv += assets.SVG_EXTERNAL_LINK + " "
        rv += html.escape(self.name)
        rv += "</a>"
        return [rv]


class Dropdown_Menu(Menu_Item):
    def __init__(self, name):
        super().__init__(name)
        self.items = []

    def add_link(self, name, target):
        self.items.append(Menu_Link(name, target))

    def generate(self, doc):
        assert isinstance(doc, Document)

        doc.style["#navbar .dropdown"] = {
            "float"    : "left",
            "overflow" : "hidden",
        }
        doc.style[".navbar-right .dropdown"] = {
            "float"    : "right",
            "overflow" : "hidden",
        }
        doc.style[".dropdown .dropbtn"] = {
            "font-size"        : "inherit",
            "border"           : "none",
            "outline"          : "none",
            "padding"          : "14px 16px",
            "background-color" : "inherit",
            "color"            : "white",
            "font-family"      : "inherit",
            "margin"           : "0",
        }
        doc.style[".dropdown:hover .dropbtn"] = {
            "background-color" : "white",
            "color"            : doc.primary_color,
        }
        doc.style[".dropdown-content"] = {
            "display"          : "none",
            "position"         : "absolute",
            "background-color" : doc.primary_color,
            "box-shadow"       : "0px 8px 16px 0px rgba(0,0,0,0.2)",
            "z-index"          : "1",
        }
        doc.style[".navbar-right .dropdown-content"] = {
            "right" : "0",
        }
        doc.style[".dropdown-content a"] = {
            "float"           : "none",
            "color"           : "white",
            "padding"         : "12px 16px",
            "text-decoration" : "none",
            "display"         : "block",
            "text-align"      : "left",
        }
        doc.style[".dropdown-content a:hover"] = {
            "color"            : doc.primary_color,
            "background-color" : "white",
        }
        doc.style[".dropdown:hover .dropdown-content"] = {
            "display"        : "flex",
            "flex-direction" : "column",
        }
        doc.style[".sticky .dropdown-content"] = {
            "position" : "fixed",
        }

        rv = ['<div class="dropdown">']
        rv.append('<button class="dropbtn">%s%s</button>' %
                  (html.escape(self.name),
                   assets.SVG_CHEVRON_DOWN))
        rv.append('<div class="dropdown-content">')
        for item in self.items:
            rv += item.generate(doc)
        rv.append("</div>")
        rv.append("</div>")
        return rv


class Navigation_Bar:
    def __init__(self):
        self.left_items  = []
        self.right_items = []

    def add_link(self, name, target, alignment="left"):
        assert alignment in ("left", "right")

        item = Menu_Link(name, target)
        if alignment == "left":
            self.left_items.append(item)
        else:
            self.right_items.append(item)

    def add_dropdown(self, name, alignment="left"):
        assert alignment in ("left", "right")

        menu = Dropdown_Menu(name)
        if alignment == "left":
            self.left_items.append(menu)
        else:
            self.right_items.append(menu)

        return menu

    def generate(self, doc):
        assert isinstance(doc, Document)

        doc.style["#navbar"] = {
            "overflow"         : "hidden",
            "background-color" : doc.primary_color,
        }
        if self.right_items:
            doc.style[".navbar-right"] = {
                "float" : "right",
            }
        doc.style["#navbar a"] = {
            "float"           : "left",
            "display"         : "block",
            "color"           : "white",
            "padding"         : "14px",
            "text-decoration" : "none",
        }
        doc.style["#navbar a:hover"] = {
            "background-color" : "white",
            "color"            : doc.primary_color,
        }
        doc.style[".sticky"] = {
            "position" : "fixed",
            "top"      : "0",
            "width"    : "100%",
        }
        doc.style[".sticky + .htmlbody"] = {
            "padding-top" : "60px",
        }

        doc.scripts.append(NAVBAR_STICKY_SCRIPT)

        rv = []

        rv.append('<div id="navbar">')
        for item in self.left_items:
            rv += item.generate(doc)
        if self.right_items:
            rv.append('<div class="navbar-right">')
            for item in self.right_items:
                rv += item.generate(doc)
            rv.append('</div>')
        rv.append('</div>')

        return rv


class Document:
    def __init__(self, title, subtitle):
        assert isinstance(title, str)
        assert isinstance(subtitle, str)
        self.title = title
        self.subtitle = subtitle

        self.primary_color = "#009ada"

        self.navbar = Navigation_Bar()
        self.style = {
            "html" : {"scroll-padding-top": "5em"},
            "body" : {"margin": "0"},
            ".title" : {
                "background-color" : self.primary_color,
                "color"            : "white",
                "padding"          : "0.5em",
                "margin"           : "0"
            },
            "h1" : {
                "padding" : "0",
                "margin"  : "0"
            },
            "h2" : {
                "padding"       : "0.5em",
                "margin"        : "0",
                "border-bottom" : "0.25em solid %s" % self.primary_color,
                "text-align"    : "right",
            },
            ".content" : {
                "padding" : "0.5em",
            },
        }
        self.scripts = []
        self.body = []

    def add_line(self, line):
        assert isinstance(line, str)
        if len(self.body) == 0:
            self.body.append('<div class="content">')
        self.body.append(line)

    def add_heading(self, level, text, anchor=None):
        assert isinstance(level, int)
        assert isinstance(text, str)
        assert 2 <= level <= 7
        assert anchor is None or isinstance(anchor, str)

        if level == 2 and self.body:
            self.body.append("</div>")

        if anchor is None:
            self.body.append("<h%u>%s</h%u>" % (level,
                                                text,
                                                level))
        else:
            self.body.append('<h%u id="sec-%s">%s</h%u>' %
                             (level,
                              anchor,
                              text,
                              level))

        if level == 2:
            self.body.append('<div class="content">')

    def render(self):
        navbar_content = self.navbar.generate(self)

        rv = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<title>%s</title>" % html.escape(self.title),
            "<style>"
        ]
        for elem, style in self.style.items():
            rv.append("%s {" % elem)
            for attr, value in style.items():
                rv.append("  %s: %s;" % (attr, value))
            rv.append("}")
        rv.append("</style>")
        rv.append("</head>")
        rv.append("<body>")

        rv.append('<div class="title">')
        rv.append("<h1>%s</h1>" % html.escape(self.title))
        rv.append('<div class="subtitle">%s</div>' %
                  html.escape(self.subtitle))
        rv.append('</div>')

        rv += navbar_content

        rv.append('<div class="htmlbody">')
        rv += self.body
        rv.append('</div>')
        rv.append('</div>')

        for script in self.scripts:
            rv.append("<script>")
            rv += script.splitlines()
            rv.append("</script>")

        rv.append("</body>")
        rv.append("</html>")

        return "\n".join(rv)
