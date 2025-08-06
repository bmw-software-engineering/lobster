#!/usr/bin/env python3
#
# lobster_html_report - Visualise LOBSTER report in HTML
# Copyright (C) 2022-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import sys
from datetime import datetime, timezone

import markdown

from lobster.html import htmldoc
from lobster.report import Report
from lobster.location import (Void_Reference,
                              File_Reference,
                              Github_Reference,
                              Codebeamer_Reference)
from lobster.items import (Tracing_Status, Item,
                           Requirement, Implementation, Activity)
from lobster.meta_data_tool_base import MetaDataToolBase

LOBSTER_GH = "https://github.com/bmw-software-engineering/lobster"


def is_dot_available(dot):
    try:
        subprocess.run([dot if dot else "dot", "-V"],
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
        rv += f"<a href='#item-{item.tag.hash()}'>{html.escape(item.name)}</a>"
    else:
        rv += html.escape(item.name)

    return rv


def create_policy_diagram(doc, report, dot):
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
        style += f', href="#sec-{name_hash(level["name"])}"'

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
        svg = subprocess.run([dot if dot else "dot", "-Tsvg", graph_name],
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
    doc.add_line("<thead><tr>")
    doc.add_line("<td>Category</td>")
    doc.add_line("<td>Ratio</td>")
    doc.add_line("<td>Coverage</td>")
    doc.add_line("<td>OK Items</td>")
    doc.add_line("<td>Total Items</td>")
    doc.add_line("</tr><thead>")
    doc.add_line("<tbody>")
    doc.add_line("</tbody>")
    for level in report.config.values():
        data = report.coverage[level["name"]]
        doc.add_line(
            f'<tr class="coverage-table-{level["name"].replace(" ", "-").lower()}">'
        )
        doc.add_line('<td><a href="#sec-%s">%s</a></td>' %
                     (name_hash(level["name"]),
                      html.escape(level["name"])))
        doc.add_line("<td>%.1f%%</td>" % data.coverage)
        doc.add_line("<td>")
        doc.add_line('<progress value="%u" max="%u">' %
                     (data.ok, data.items))
        doc.add_line("%.2f%%" % data.coverage)
        doc.add_line('</progress>')
        doc.add_line("</td>")
        doc.add_line('<td align="right">%u</td>' % data.ok)
        doc.add_line('<td align="right">%u</td>' % data.items)
        doc.add_line("</tr>")
    doc.add_line("</table>")


def run_git_show(commit_hash, path=None):
    """Run `git show` command to get the commit timestamp."""
    cmd = ['git'] + (['-C', path] if path else []) + [
        'show', '-s', '--format=%ct', commit_hash]
    try:
        output = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if output.stdout.strip():
            epoch = int(output.stdout.strip())
            return str(datetime.fromtimestamp(epoch, tz=timezone.utc)) + " UTC"
    except subprocess.CalledProcessError:
        location = f"submodule path: {path}" if path else "main repository"
        print(f"[Warning] Could not find commit {commit_hash} in {location}.")
    return None


def get_commit_timestamp_utc(commit_hash, submodule_path=None):
    """Get commit timestamp in UTC format, either from main repo or submodule."""
    timestamp = run_git_show(commit_hash)
    if timestamp:
        return f"{timestamp}"

    if submodule_path:
        timestamp = run_git_show(commit_hash, submodule_path)
        if timestamp:
            return f"{timestamp} (from submodule at {submodule_path})"

    return "Unknown"


def write_item_box_begin(doc, item):
    assert isinstance(doc, htmldoc.Document)
    assert isinstance(item, Item)

    doc.add_line(f'<!-- begin item {html.escape(item.tag.key())} -->')

    doc.add_line(f'<div class="item-{html.escape(item.tracing_status.name.lower())}" '
                 f'id="item-{item.tag.hash()}">')

    doc.add_line('<div class="item-name">%s %s</div>' %
                 ('<svg class="icon"><use href="#svg-check-square"></use></svg>'
                  if item.tracing_status in (Tracing_Status.OK,
                                             Tracing_Status.JUSTIFIED)
                  else '<svg class="icon"><use href="#svg-alert-triangle"></use></svg>',
                  xref_item(item, link=False)))

    doc.add_line('<div class="attribute">Source: ')
    doc.add_line('<svg class="icon"><use href="#svg-external-link"></use></svg>')

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


def write_item_box_end(doc, item):
    assert isinstance(doc, htmldoc.Document)

    if getattr(item.location, "commit", None) is not None:
        commit_hash = item.location.commit
        timestamp = get_commit_timestamp_utc(commit_hash, item.location.gh_repo)
        doc.add_line(
            f'<div class="attribute">'
            f'Build Reference: <strong>{commit_hash}</strong> | '
            f'Timestamp: {timestamp}'
            f'</div>'
        )
    doc.add_line("</div>")
    doc.add_line('<!-- end item -->')


def generate_custom_data(report) -> str:
    content = [
        f"{key}: {value}<br>"
        for key, value in report.custom_data.items()
        if value
    ]
    return "".join(content)


def write_html(fd, report, dot, high_contrast, render_md):
    assert isinstance(report, Report)

    doc = htmldoc.Document(
        "L.O.B.S.T.E.R.",
        "Lightweight Open BMW Software Traceability Evidence Report"
    )

    # Item styles
    doc.style["#custom-data-banner"] = {
        "position": "absolute",
        "top": "1em",
        "right": "2em",
        "font-size": "0.9em",
        "color": "white",
    }
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
        "background-color" : "#b2e1b2" if high_contrast else "#efe",
    }
    doc.style[".item-partial"] = {
        "background-color" : "#ffe",
    }
    doc.style[".item-missing"] = {
        "background-color" : "#ffb2ff" if high_contrast else "#fee",
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

    # Render MD
    if render_md:
        doc.style[".md_description"] = {
            "font-style" : "unset",
        }
        doc.style[".md_description h1"] = {
            "padding" : "unset",
            "margin"  : "unset"
        }
        doc.style[".md_description h2"] = {
            "padding"       : "unset",
            "margin"        : "unset",
            "border-bottom" : "unset",
            "text-align"    : "unset"
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

    ### Menu & Navigation
    doc.navbar.add_link("Overview", "#sec-overview")
    doc.navbar.add_link("Issues", "#sec-issues")
    menu = doc.navbar.add_dropdown("Detailed report")
    for level in report.config.values():
        menu.add_link(level["name"], "#sec-" + name_hash(level["name"]))
    # doc.navbar.add_link("Software Traceability Matrix", "#matrix")
    if report.custom_data:
        content = generate_custom_data(report)
        doc.add_line(f'<div id="custom-data-banner">{content}</div>')
    menu = doc.navbar.add_dropdown("LOBSTER", "right")
    menu.add_link("Documentation",
                  "%s/blob/main/README.md" % LOBSTER_GH)
    menu.add_link("License",
                  "%s/blob/main/LICENSE.md" % LOBSTER_GH)
    menu.add_link("Source", LOBSTER_GH)

    ### Summary (Coverage & Policy)
    doc.add_heading(2, "Overview", "overview", html_identifier=True)
    doc.add_line('<div class="columns">')
    doc.add_line('<div class="column">')
    doc.add_heading(3, "Coverage", html_identifier=True)
    create_item_coverage(doc, report)
    doc.add_line('</div>')
    if is_dot_available(dot):
        doc.add_line('<div class="column">')
        doc.add_heading(3, "Tracing policy")
        create_policy_diagram(doc, report, dot)
        doc.add_line('</div>')
    else:
        print("warning: dot utility not found, report will not "
              "include the tracing policy visualisation")
        print("> please install Graphviz (https://graphviz.org)")
    doc.add_line('</div>')

    ### Filtering
    doc.add_heading(2, "Filtering", "filtering-options", html_identifier=True)
    doc.add_heading(3, "Item Filters", html_identifier=True)
    doc.add_line('<div id = "btnFilterItem">')
    doc.add_line('<button class="button buttonAll buttonActive" '
                 'onclick="buttonFilter(\'all\')"> Show All </button>')

    doc.add_line('<button class ="button buttonOK" '
                 'onclick="buttonFilter(\'ok\')" > OK </button>')

    doc.add_line('<button class ="button buttonMissing" '
                 'onclick="buttonFilter(\'missing\')" > Missing </button>')

    doc.add_line('<button class ="button buttonPartial" '
                 'onclick="buttonFilter(\'partial\')" > Partial </button>')

    doc.add_line('<button class ="button buttonJustified" '
                 'onclick="buttonFilter(\'justified\')" > Justified </button>')

    doc.add_line('<button class ="button buttonWarning" '
                 'onclick="buttonFilter(\'warning\')" > Warning </button>')
    doc.add_line("</div>")

    doc.add_heading(3, "Show Issues", html_identifier=True)
    doc.add_line('<div id = "ContainerBtnToggleIssue">')
    doc.add_line('<button class ="button buttonBlue" id="BtnToggleIssue" '
                 'onclick="ToggleIssues()"> Show Issues </button>')
    doc.add_line('</div>')

    doc.add_heading(3, "Filter", "filter", html_identifier=True)
    doc.add_line('<input type="text" id="search" placeholder="Filter..." '
                 'onkeyup="searchItem()">')
    doc.add_line('<div id="search-sec-id"')

    ### Issues
    doc.add_heading(2, "Issues", "issues", html_identifier=True)
    doc.add_line('<div id="issues-section" style="display:none">')
    has_issues = False
    for item in sorted(report.items.values(),
                       key = lambda x: x.location.sorting_key()):
        if item.tracing_status not in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
            for message in item.messages:
                if not has_issues:
                    has_issues = True
                    doc.add_line("<ul>")
                doc.add_line(
                    f'<li class="issue issue-{item.tracing_status.name.lower()}-'
                    f'{item.tag.namespace}">{xref_item(item)}: {message}</li>'
                )
    if has_issues:
        doc.add_line("</ul>")
    else:
        doc.add_line("<div>No traceability issues found.</div>")
    doc.add_line("</div>")

    ### Report
    file_heading = None
    doc.add_heading(2, "Detailed report", "detailed-report", html_identifier=True)
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
        doc.add_line(f'<div class="detailed-report-{title.lower().replace(" ", "-")}">')
        doc.add_heading(3, title, html_identifier=True)
        for level in report.config.values():
            if level["kind"] != kind:
                continue
            doc.add_heading(4,
                            html.escape(level["name"]),
                            name_hash(level["name"]),
                            html_identifier=True,
                            )
            if items_by_level[level["name"]]:
                for item in sorted(items_by_level[level["name"]],
                                   key = lambda x: x.location.sorting_key()):
                    if isinstance(item.location, Void_Reference):
                        new_file_heading = "Unknown"
                    elif isinstance(item.location, (File_Reference,
                                                    Github_Reference)):
                        new_file_heading = item.location.filename
                    elif isinstance(item.location, Codebeamer_Reference):
                        new_file_heading = "Codebeamer %s, tracker %u" % \
                            (item.location.cb_root,
                             item.location.tracker)
                    else:  # pragma: no cover
                        assert False
                    if new_file_heading != file_heading:
                        file_heading = new_file_heading
                        doc.add_heading(5, html.escape(file_heading),
                                        html_identifier=True)

                    write_item_box_begin(doc, item)
                    if isinstance(item, Requirement) and item.status:
                        doc.add_line('<div class="attribute">')
                        doc.add_line("Status: %s" % html.escape(item.status))
                        doc.add_line('</div>')
                    if isinstance(item, Requirement) and item.text:
                        if render_md:
                            bq_class = ' class="md_description"'
                            bq_text = markdown.markdown(item.text,
                                                        extensions=['tables'])
                        else:
                            bq_class = ""
                            bq_text = html.escape(item.text).replace("\n", "<br>")

                        doc.add_line('<div class="attribute">')
                        doc.add_line(f"<blockquote{bq_class}>{bq_text}</blockquote>")
                        doc.add_line('</div>')
                    write_item_tracing(doc, report, item)
                    write_item_box_end(doc, item)
            else:
                doc.add_line("No items recorded at this level.")
        doc.add_line("</div>")  # Closing tag for detailed-report-<title>
    # Closing tag for id #search-sec-id
    doc.add_line("</div>")

    # Add the css from assets
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = dir_path + "/assets"
    for filename in os.listdir(file_path):
        if filename.endswith(".css"):
            filename = os.path.join(file_path, filename)
            with open(filename, "r", encoding="UTF-8") as styles:
                doc.css.append("".join(styles.readlines()))

    # Add javascript from assets/html_report.js file
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = dir_path + "/assets"
    for filename in os.listdir(file_path):
        if filename.endswith(".js"):
            filename = os.path.join(file_path, filename)
            with open(filename, "r", encoding="UTF-8") as scripts:
                doc.scripts.append("".join(scripts.readlines()))

    fd.write(doc.render() + "\n")


class HtmlReportTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="html-report",
            description="Visualise LOBSTER report in HTML",
            official=True,
        )

        ap = self._argument_parser
        ap.add_argument("lobster_report",
                        nargs="?",
                        default="report.lobster")
        ap.add_argument("--out",
                        default="lobster_report.html")
        ap.add_argument("--dot",
                        help="path to dot utility (https://graphviz.org), \
                        by default expected in PATH",
                        default=None)
        ap.add_argument("--high-contrast",
                        action="store_true",
                        help="Uses a color palette with a higher contrast.")
        ap.add_argument("--render-md",
                        action="store_true",
                        help="Renders MD in description.")

    def _run_impl(self, options: argparse.Namespace) -> int:
        if not os.path.isfile(options.lobster_report):
            self._argument_parser.error(f"{options.lobster_report} is not a file")

        report = Report()
        report.load_report(options.lobster_report)

        with open(options.out, "w", encoding="UTF-8") as fd:
            write_html(
                fd = fd,
                report = report,
                dot = options.dot,
                high_contrast = options.high_contrast,
                render_md = options.render_md,
            )
            print("LOBSTER HTML report written to %s" % options.out)

        return 0


def main() -> int:
    return HtmlReportTool().run()


if __name__ == "__main__":
    sys.exit(main())
