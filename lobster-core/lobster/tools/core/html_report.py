#!/usr/bin/env python3
#
# lobster_html_report - Visualise LOBSTER report in HTML
# Copyright (C) 2022-2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import os.path
import argparse
import html
import subprocess
import hashlib
import tempfile

from lobster.html import htmldoc, assets
from lobster.report import Report
from lobster.items import (Tracing_Status, Item,
                           Requirement, Implementation, Activity)

LOBSTER_GH = "https://github.com/bmw-software-engineering/lobster"


def is_dot_available():
    try:
        subprocess.run(["dot", "-V"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       encoding="UTF-8",
                       check=True)
        return True
    except FileNotFoundError:
        return False


def name_hash(name):
    hobj = hashlib.md5()
    hobj.update(name.encode("UTF-8"))
    return hobj.hexdigest()


# def write_stm(doc, xref, levels, stm):
#     assert isinstance(doc, htmldoc.Document)

#     doc.add_line('<table width="100%">')
#     doc.add_line("<thead>")
#     doc.add_line("<tr>")
#     for level in levels:
#         doc.add_line("<td>%s</td>" % html.escape(level["name"]))
#     doc.add_line("</tr>")
#     doc.add_line("</thead>")
#     doc.add_line("<tbody>")
#     for n, row in enumerate(stm):
#         if n % 2:
#             doc.add_line("<tr>")
#         else:
#             doc.add_line('<tr class="alt">')
#         for level in levels:
#             doc.add_line("<td>")
#             for item_name in row[level["name"]]:
#                 doc.add_line(
#                     '<div class="subtle-%s">%s</div>' %
#                     (xref[item_name]["tracing_status"].lower(),
#                      xref_item(xref, item_name,
#                                brief = level["kind"] != "implementation")))
#             doc.add_line("</td>")
#         doc.add_line("</tr>")
#     doc.add_line("</tbody>")
#     doc.add_line("</table>")


def xref_item(item, link=True, brief=False):
    assert isinstance(item, Item)
    assert isinstance(link, bool)
    assert isinstance(brief, bool)

    if brief:
        rv = ""
    elif isinstance(item, Requirement):
        rv = html.escape(item.framework + " " +
                         item.kind.capitalize())
    elif isinstance(item, Implementation):
        rv = html.escape(item.language + " " +
                         item.kind.capitalize())
    else:
        assert isinstance(item, Activity)
        rv = html.escape(item.framework + " " +
                         item.kind.capitalize())
    if not brief:
        rv += " "

    if link:
        rv += "<a href='#item-%s'>%s</a>" % (item.tag.hash(),
                                             item.name)
    else:
        rv += "%s" % item.name

    return rv


def create_policy_diagram(doc, report):
    assert isinstance(doc, htmldoc.Document)
    assert isinstance(report, Report)

    graph = 'digraph "LOBSTER Tracing Policy" {\n'
    for level in report.config.values():
        if level["kind"] == "requirements":
            style = 'shape=box, style=rounded'
        elif level["kind"] == "implementation":
            style = 'shape=box'
        else:
            assert level["kind"] == "activity"
            style = 'shape=hexagon'
        style += ', href="#sec-%s"' % name_hash(level["name"])

        graph += '  n_%s [label="%s", %s];\n' % \
            (name_hash(level["name"]),
             level["name"],
             style)

    for level in report.config.values():
        source = name_hash(level["name"])
        for target in map(name_hash, level["traces"]):
            # Not a mistake; we want to show the tracing down, whereas
            # in the config file we indicate how we trace up.
            graph += '  n_%s -> n_%s;\n' % (target, source)
    graph += "}\n"

    with tempfile.TemporaryDirectory() as tmp_dir:
        graph_name = os.path.join(tmp_dir, "graph.dot")
        with open(graph_name, "w", encoding="UTF-8") as tmp_fd:
            tmp_fd.write(graph)
        svg = subprocess.run(["dot", "-Tsvg", graph_name],
                             stdout=subprocess.PIPE,
                             encoding="UTF-8",
                             check=True)
        assert svg.returncode == 0
        image = svg.stdout[svg.stdout.index("<svg "):]

    for line in image.splitlines():
        doc.add_line(line)


def create_item_coverage(doc, report):
    assert isinstance(doc, htmldoc.Document)
    assert isinstance(report, Report)

    doc.add_line("<table>")
    doc.add_line("<thead><tr><td>Category</td><td>Coverage</td></tr><thead>")
    doc.add_line("<tbody>")
    doc.add_line("</tbody>")
    for level in report.config.values():
        coverage = report.coverage[level["name"]]["coverage"]
        doc.add_line("<tr>")
        doc.add_line('<td><a href="#sec-%s">%s</a></td>' %
                     (name_hash(level["name"]),
                      html.escape(level["name"])))
        doc.add_line("<td>")
        doc.add_line('<div class="progress-bar">')
        doc.add_line('<div class="bar" style="width:%f%%;">' %
                     coverage)
        doc.add_line("%.1f%%" % coverage)
        doc.add_line("</div>")
        doc.add_line("</div>")
        doc.add_line("</td>")
        doc.add_line("</tr>")
    doc.add_line("</table>")


def write_item_box_begin(doc, item):
    assert isinstance(doc, htmldoc.Document)
    assert isinstance(item, Item)

    doc.add_line('<!-- begin item %s -->' % html.escape(item.tag.key()))

    doc.add_line('<div class="item-%s" id="item-%s">' %
                 (item.tracing_status.name.lower(),
                  item.tag.hash()))

    doc.add_line('<div class="item-name">%s %s</div>' %
                 (assets.SVG_CHECK_SQUARE
                  if item.tracing_status in (Tracing_Status.OK,
                                             Tracing_Status.JUSTIFIED)
                  else assets.SVG_ALERT_TRIANGLE,
                  xref_item(item, link=False)))

    doc.add_line('<div class="attribute">Source: ')
    doc.add_line(assets.SVG_EXTERNAL_LINK)
    doc.add_line(item.location.to_html())
    doc.add_line("</div>")


def write_item_tracing(doc, report, item):
    assert isinstance(doc, htmldoc.Document)
    assert isinstance(report, Report)
    assert isinstance(item, Item)

    doc.add_line('<div class="attribute">')
    if item.ref_down:
        doc.add_line("<div>Traces to:")
        doc.add_line("<ul>")
        for ref in item.ref_down:
            doc.add_line("<li>%s</li>" % xref_item(report.items[ref.key()]))
        doc.add_line("</ul>")
        doc.add_line("</div>")
    if item.ref_up:
        doc.add_line("<div>Derived from:")
        doc.add_line("<ul>")
        for ref in item.ref_up:
            doc.add_line("<li>%s</li>" % xref_item(report.items[ref.key()]))
        doc.add_line("</ul>")
        doc.add_line("</div>")

    if item.tracing_status == Tracing_Status.JUSTIFIED:
        doc.add_line("<div>Justifications:")
        doc.add_line("<ul>")
        for msg in item.just_global + item.just_up + item.just_down:
            doc.add_line("<li>%s</li>" % html.escape(msg))
        doc.add_line("</ul>")
        doc.add_line("</div>")

    if item.messages:
        doc.add_line("<div>Issues:")
        doc.add_line("<ul>")
        for msg in item.messages:
            doc.add_line("<li>%s</li>" % html.escape(msg))
        doc.add_line("</ul>")
        doc.add_line("</div>")

    doc.add_line("</div>")


def write_item_box_end(doc):
    assert isinstance(doc, htmldoc.Document)
    doc.add_line("</div>")
    doc.add_line('<!-- end item -->')


def write_html(fd, report):
    assert isinstance(report, Report)

    doc = htmldoc.Document(
        "L.O.B.S.T.E.R.",
        "Lightweight Open BMW Software Tracability Evidence Report"
    )

    # Item styles
    doc.style[".item-ok, .item-partial, .item-missing, .item-justified"] = {
        "border"        : "1px solid black",
        "border-radius" : "0.5em",
        "margin-top"    : "0.4em",
        "padding"       : "0.25em",
    }
    doc.style[".item-ok:target, "
              ".item-partial:target, "
              ".item-missing:target, "
              ".item-justified:target"] = {
        "border" : "3px solid black",
    }
    doc.style[".subtle-ok, "
              ".subtle-partial, "
              ".subtle-missing, "
              ".subtle-justified"] = {
        "padding-left"  : "0.2em",
    }
    doc.style[".item-ok"] = {
        "background-color" : "#efe",
    }
    doc.style[".item-partial"] = {
        "background-color" : "#ffe",
    }
    doc.style[".item-missing"] = {
        "background-color" : "#fee",
    }
    doc.style[".item-justified"] = {
        "background-color" : "#eee",
    }
    doc.style[".subtle-ok"] = {
        "border-left" : "0.2em solid #8f8",
    }
    doc.style[".subtle-partial"] = {
        "border-left" : "0.2em solid #ff8",
    }
    doc.style[".subtle-missing"] = {
        "border-left" : "0.2em solid #f88",
    }
    doc.style[".subtle-justified"] = {
        "border-left" : "0.2em solid #888",
    }
    doc.style[".item-name"] = {
        "font-size" : "125%",
        "font-weight" : "bold",
    }
    doc.style[".attribute"] = {
        "margin-top" : "0.5em",
    }

    # Columns
    doc.style[".columns"] = {
        "display" : "flex",
    }
    doc.style[".columns .column"] = {
        "flex" : "45%",
    }

    # Tables
    doc.style["thead tr"] = {
        "font-weight" : "bold",
    }
    doc.style["tbody tr.alt"] = {
        "background-color" : "#eee",
    }

    # Text
    doc.style["blockquote"] = {
        "font-style"   : "italic",
        "border-left"  : "0.2em solid gray",
        "padding-left" : "0.4em",
        "margin-left"  : "0.5em",
    }

    # Progress bars
    doc.style[".progress-bar"] = {
        "width"            : "20em",
        "background-color" : "#aaa",
        "border-left"      : "1px solid #888",
        "border-top"       : "1px solid #888",
        "border-right"     : "1px solid #ccc",
        "border-bottom"    : "1px solid #ccc",
        "padding"          : "0",
        "margin"           : "0.25em",
        "border-radius"    : "5px",
    }
    doc.style[".progress-bar .bar"] = {
        "background-color" : doc.primary_color,
        "color"            : "white",
        "margin"           : "0",
        "padding-top"      : "0.2em",
        "padding-bottom"   : "0.2em",
        "text-align"       : "center",
        "border-radius"    : "5px",
    }

    ### Menu & Navigation
    doc.navbar.add_link("Overview", "#sec-overview")
    doc.navbar.add_link("Issues", "#sec-issues")
    menu = doc.navbar.add_dropdown("Detailed report")
    for level in report.config.values():
        menu.add_link(level["name"], "#sec-" + name_hash(level["name"]))
    # doc.navbar.add_link("Software Traceability Matrix", "#matrix")
    menu = doc.navbar.add_dropdown("LOBSTER", "right")
    menu.add_link("Documentation",
                  "%s/blob/main/README.md" % LOBSTER_GH)
    menu.add_link("License",
                  "%s/blob/main/LICENSE.md" % LOBSTER_GH)
    menu.add_link("Source", LOBSTER_GH)

    ### Summary (Coverage & Policy)
    doc.add_heading(2, "Overview", "overview")
    doc.add_line('<div class="columns">')
    doc.add_line('<div class="column">')
    doc.add_heading(3, "Coverage")
    create_item_coverage(doc, report)
    doc.add_line('</div>')
    if is_dot_available():
        doc.add_line('<div class="column">')
        doc.add_heading(3, "Tracing policy")
        create_policy_diagram(doc, report)
        doc.add_line('</div>')
    else:
        print("warning: dot utility not found, report will not "
              "include the tracing policy visualisation")
        print("> please install Graphviz (https://graphviz.org)")
    doc.add_line('</div>')

    ### Issues
    doc.add_heading(2, "Issues", "issues")
    has_issues = False
    for item in report.items.values():
        if item.tracing_status not in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
            for message in item.messages:
                if not has_issues:
                    has_issues = True
                    doc.add_line("<ul>")
                doc.add_line("<li>%s: %s</li>" %
                             (xref_item(item),
                              message))
    if has_issues:
        doc.add_line("</ul>")
    else:
        doc.add_line("<div>No tracability issues found.</div>")

    ### Report
    doc.add_heading(2, "Detailed report", "detailed-report")
    items_by_level = {}
    for level in report.config:
        items_by_level[level] = [item
                                 for item in report.items.values()
                                 if item.level == level]
    for kind, title in [("requirements",
                         "Requirements and Specification"),
                        ("implementation",
                         "Implementation"),
                        ("activity",
                         "Verification and Validation")]:
        doc.add_heading(3, title)
        for level in report.config.values():
            if level["kind"] != kind:
                continue
            doc.add_heading(4,
                            html.escape(level["name"]),
                            name_hash(level["name"]))

            if items_by_level[level["name"]]:
                for item in items_by_level[level["name"]]:
                    write_item_box_begin(doc, item)
                    if isinstance(item, Requirement) and item.status:
                        doc.add_line('<div class="attribute">')
                        doc.add_line("Status: %s" % html.escape(item.status))
                        doc.add_line('</div>')
                    if isinstance(item, Requirement) and item.text:
                        doc.add_line('<div class="attribute">')
                        doc.add_line("<blockquote>%s</blockquote>" %
                                     html.escape(item.text))
                        doc.add_line('</div>')
                    write_item_tracing(doc, report, item)
                    write_item_box_end(doc)
            else:
                doc.add_line("No items recorded at this level.")

    ### STM
    # doc.add_heading(2, "Software traceability matrix", "matrix")
    # write_stm(doc, xref, levels, stm)

    fd.write(doc.render() + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lobster_report",
                    nargs="?",
                    default="report.lobster")
    ap.add_argument("--out",
                    default="lobster_report.html")
    options = ap.parse_args()

    if not os.path.isfile(options.lobster_report):
        if options.lobster_report == "report.lobster":
            ap.error("specify report file")
        else:
            ap.error("%s is not a file" % options.lobster_report)

    report = Report()
    report.load_report(options.lobster_report)

    with open(options.out, "w", encoding="UTF-8") as fd:
        write_html(fd     = fd,
                   report = report)
        print("LOBSTER HTML report written to %s" % options.out)


if __name__ == "__main__":
    main()
