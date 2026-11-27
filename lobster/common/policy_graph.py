# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
"""Dependency-free layered SVG rendering of a tracing policy."""

import html
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

NODE_HEIGHT = 72
MIN_NODE_WIDTH = 240
CHAR_WIDTH = 10
NODE_PADDING = 116
LAYER_GAP = 80
ROW_GAP = 26
COLUMN_GAP = 32
LAYER_GAP_VERTICAL = 60
MARGIN = 16
ORDERING_SWEEPS = 4
GAUGE_RADIUS = 24

EDGE_COLOR = "#64748b"
NODE_ACCENT = "#719fbd"


@dataclass(frozen=True)
class PolicyNode:
    identifier: str
    label: str
    href: str = ""
    detail: str = ""
    ratio: Optional[float] = None


@dataclass(frozen=True)
class PolicyEdge:
    source: str
    target: str


def _find_back_edges(
    identifiers: Sequence[str],
    edges: Sequence[PolicyEdge],
) -> Set[Tuple[str, str]]:
    """Return the edges that close a cycle, including self loops."""
    successors: Dict[str, List[str]] = {i: [] for i in identifiers}
    for edge in edges:
        successors[edge.source].append(edge.target)

    back_edges: Set[Tuple[str, str]] = set()
    on_stack: Set[str] = set()
    visited: Set[str] = set()

    def visit(node: str) -> None:
        visited.add(node)
        on_stack.add(node)
        for target in successors[node]:
            if target in on_stack:
                back_edges.add((node, target))
            elif target not in visited:
                visit(target)
        on_stack.discard(node)

    for identifier in identifiers:
        if identifier not in visited:
            visit(identifier)
    return back_edges


def compute_layers(
    identifiers: Sequence[str],
    edges: Sequence[PolicyEdge],
) -> List[List[str]]:
    """Assign each node to the layer given by its longest path from a root.

    Edges that close a cycle are ignored. Within a layer, nodes are ordered
    to reduce edge crossings.
    """
    back_edges = _find_back_edges(identifiers, edges)
    forward = [e for e in edges if (e.source, e.target) not in back_edges]
    predecessors: Dict[str, List[str]] = {i: [] for i in identifiers}
    successors: Dict[str, List[str]] = {i: [] for i in identifiers}
    for edge in forward:
        predecessors[edge.target].append(edge.source)
        successors[edge.source].append(edge.target)

    depth: Dict[str, int] = {}

    def depth_of(node: str) -> int:
        if node not in depth:
            depth[node] = max(
                (depth_of(p) + 1 for p in predecessors[node]), default=0
            )
        return depth[node]

    for identifier in identifiers:
        depth_of(identifier)

    layers: List[List[str]] = [[] for _ in range(max(depth.values(), default=-1) + 1)]
    for identifier in identifiers:
        layers[depth[identifier]].append(identifier)

    def reorder(layer_index: int, neighbours: Dict[str, List[str]],
                reference_index: int) -> None:
        position = {n: i for i, n in enumerate(layers[reference_index])}
        current = {n: i for i, n in enumerate(layers[layer_index])}

        def barycenter(node: str) -> float:
            known = [position[n] for n in neighbours[node] if n in position]
            return sum(known) / len(known) if known else current[node]

        layers[layer_index].sort(key=barycenter)

    for _ in range(ORDERING_SWEEPS):
        for index in range(1, len(layers)):
            reorder(index, predecessors, index - 1)
        for index in range(len(layers) - 2, -1, -1):
            reorder(index, successors, index + 1)
    return layers


def _node_width(node: PolicyNode) -> float:
    longest = max(len(node.label) * CHAR_WIDTH, len(node.detail) * 7.5)
    return max(MIN_NODE_WIDTH, longest + NODE_PADDING)


def _bar_color(ratio: float) -> str:
    if ratio >= 100:
        return "#2e9e5b"
    if ratio >= 50:
        return "#e39a1c"
    return "#d9534f"


def _node_shape(x: float, y: float, width: float) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" '
            f'height="{NODE_HEIGHT}" rx="8" fill="#ffffff" '
            'stroke="#d7e0e5" stroke-width="1" '
            'filter="url(#policy-shadow)"/>')


def render_svg(
    nodes: Sequence[PolicyNode],
    edges: Sequence[PolicyEdge],
    vertical: bool = True,
) -> str:
    """Render the policy as an SVG document, edges pointing from source to target.

    Layers are stacked top to bottom if vertical, otherwise left to right.
    """
    by_id = {n.identifier: n for n in nodes}
    valid_edges = [e for e in edges if e.source in by_id and e.target in by_id]
    layers = compute_layers([n.identifier for n in nodes], valid_edges)

    boxes: Dict[str, Tuple[float, float, float]] = {}
    if vertical:
        row_widths = [
            sum(_node_width(by_id[i]) for i in layer) + (len(layer) - 1) * COLUMN_GAP
            for layer in layers
        ]
        content_width = max(row_widths, default=0)
        y = MARGIN
        for layer, row_width in zip(layers, row_widths):
            x = MARGIN + (content_width - row_width) / 2
            for identifier in layer:
                width = _node_width(by_id[identifier])
                boxes[identifier] = (x, y, width)
                x += width + COLUMN_GAP
            y += NODE_HEIGHT + LAYER_GAP_VERTICAL
        total_width = max(content_width + 2 * MARGIN, 2 * MARGIN)
        total_height = max(y - LAYER_GAP_VERTICAL + MARGIN, 2 * MARGIN)
    else:
        layer_widths = [max(_node_width(by_id[i]) for i in layer)
                        for layer in layers]
        tallest = max((len(layer) for layer in layers), default=0)
        content_height = tallest * NODE_HEIGHT + max(tallest - 1, 0) * ROW_GAP
        x = MARGIN
        for layer, layer_width in zip(layers, layer_widths):
            layer_height = len(layer) * NODE_HEIGHT + (len(layer) - 1) * ROW_GAP
            y = MARGIN + (content_height - layer_height) / 2
            for identifier in layer:
                width = _node_width(by_id[identifier])
                boxes[identifier] = (x + (layer_width - width) / 2, y, width)
                y += NODE_HEIGHT + ROW_GAP
            x += layer_width + LAYER_GAP
        total_width = max(x - LAYER_GAP + MARGIN, 2 * MARGIN)
        total_height = content_height + 2 * MARGIN

    back_edges = _find_back_edges([n.identifier for n in nodes], valid_edges)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.0f}" '
        f'height="{total_height:.0f}" '
        f'viewBox="0 0 {total_width:.0f} {total_height:.0f}" '
        f'style="max-width:100%;height:auto" '
        f'role="img" aria-label="LOBSTER Tracing Policy">',
        "<title>LOBSTER Tracing Policy</title>",
        '<defs>'
        '<marker id="policy-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" '
        'orient="auto">'
        f'<path d="M 0 1 L 10 5 L 0 9 z" fill="{EDGE_COLOR}"/></marker>'
        '<filter id="policy-shadow" x="-10%" y="-10%" width="125%" height="150%">'
        '<feDropShadow dx="0" dy="3" stdDeviation="3" flood-opacity="0.18"/>'
        '</filter></defs>',
        '<style>a{cursor:pointer}a:hover{opacity:0.9}</style>',
    ]

    for edge in valid_edges:
        sx, sy, sw = boxes[edge.source]
        tx, ty, tw = boxes[edge.target]
        dashed = ""
        if (edge.source, edge.target) in back_edges:
            dashed = ' stroke-dasharray="5,3"'
        if edge.source == edge.target:
            right = sx + sw
            top = sy
            path = (f"M {right - 10:.1f} {top:.1f} "
                    f"L {right - 10:.1f} {top - 12:.1f} "
                    f"L {right + 10:.1f} {top - 12:.1f} "
                    f"L {right + 10:.1f} {top + 12:.1f} "
                    f"L {right:.1f} {top + 12:.1f}")
        elif vertical:
            if (edge.source, edge.target) in back_edges:
                start_y, end_y = sy, ty + NODE_HEIGHT
            else:
                start_y, end_y = sy + NODE_HEIGHT, ty
            start_x, end_x = sx + sw / 2, tx + tw / 2
            path = (f"M {start_x:.1f} {start_y:.1f} "
                    f"L {end_x:.1f} {end_y:.1f}")
        elif tx >= sx + sw:
            start_x, end_x = sx + sw, tx
            path = (f"M {start_x:.1f} {sy + NODE_HEIGHT / 2:.1f} "
                    f"L {end_x:.1f} {ty + NODE_HEIGHT / 2:.1f}")
        else:
            start_x, end_x = sx, tx + tw
            path = (f"M {start_x:.1f} {sy + NODE_HEIGHT / 2:.1f} "
                    f"L {end_x:.1f} {ty + NODE_HEIGHT / 2:.1f}")
        out.append(f'<path d="{path}" fill="none" stroke="{EDGE_COLOR}" '
                   f'stroke-width="1.8"{dashed} '
                   f'marker-end="url(#policy-arrow)"/>')

    for node in nodes:
        nx, ny, nw = boxes[node.identifier]
        font = 'font-family="Verdana,DejaVu Sans,sans-serif"'
        text_x = nx + 16
        has_extra = bool(node.detail)
        title_y = ny + (30 if has_extra else NODE_HEIGHT / 2 + 6)
        text_color = "#101820"
        group = [
            _node_shape(nx, ny, nw),
            f'<rect x="{nx:.1f}" y="{ny + 8:.1f}" width="8" '
            f'height="{NODE_HEIGHT - 16}" rx="4" '
            f'fill="{NODE_ACCENT}"/>',
            f'<text x="{text_x:.1f}" y="{title_y:.1f}" {font} '
            f'font-size="16" font-weight="bold" fill="{text_color}">'
            f'{html.escape(node.label)}</text>',
        ]
        if node.detail:
            group.append(
                f'<text x="{text_x:.1f}" y="{ny + 51:.1f}" {font} '
                f'font-size="13" fill="{text_color}">{html.escape(node.detail)}</text>')
        if node.ratio is not None:
            percent = max(0.0, min(node.ratio, 100.0))
            gx, gy = nx + nw - 38, ny + NODE_HEIGHT / 2
            circumference = 2 * 3.141592653589793 * GAUGE_RADIUS
            group.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="28" fill="#ffffff"/>')
            group.append(
                f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{GAUGE_RADIUS}" '
                f'fill="none" stroke="#e5e7eb" stroke-width="4"/>')
            if percent > 0:
                group.append(
                    f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{GAUGE_RADIUS}" '
                    f'fill="none" stroke="{_bar_color(percent)}" stroke-width="4" '
                    f'stroke-linecap="round" '
                    f'stroke-dasharray="{circumference * percent / 100:.1f} '
                    f'{circumference:.1f}" '
                    f'transform="rotate(-90 {gx:.1f} {gy:.1f})"/>')
            group.append(
                f'<text x="{gx:.1f}" y="{gy + 4:.1f}" text-anchor="middle" {font} '
                f'font-size="11" font-weight="bold" fill="#1f2933">'
                f'{percent:.0f}%</text>')
        if node.href:
            out.append(f'<a href="{html.escape(node.href, quote=True)}">')
            out.extend(group)
            out.append("</a>")
        else:
            out.extend(group)

    out.append("</svg>")
    return "\n".join(out)
