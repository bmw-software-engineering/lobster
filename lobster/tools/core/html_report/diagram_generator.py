import hashlib
from typing import Optional, Tuple
from xml.etree import ElementTree as ET
import plotly.graph_objects as go

from lobster.htmldoc import htmldoc
from lobster.common.report import Report

# Node layout constants
NODE_SPACING_X = 0.8                  # Horizontal spacing between nodes
DEFAULT_NODE_X = 0.5                  # Default horizontal center for node placement
Y_POSITIONS = {"requirements": 1.0, "implementation": 0.6, "activity": 0.2}
DEFAULT_FONT_SIZE = 11
OPACITY = 0.85

# Node appearance constants
CHAR_WIDTH = 0.02                     # Estimated width per character for node sizing
NODE_HEIGHT = 0.2                     # Fixed node height
NODE_LABEL_FONT_SIZE = 12             # Font size for node labels
NODE_MIN_WIDTH = 0.28                 # Minimum width for node rectangles
NODE_LABEL_PADDING = 0.1              # Extra padding added to node width for label

# Arrow constants
ARROW_CURVE_AMOUNT_BIDIRECTIONAL = 0.08     # Amount of curve for bidirectional
ARROW_CURVE_AMOUNT_NON_BIDIRECTIONAL = 0.4  # Amount of curve for non-bidirectional
ARROW_SHORTEN_FACTOR = 0.9                  # Factor to shorten arrowhead along curve
DEFAULT_ARROW_LABEL = "trace to"            # Default label for arrows if not specified

# Figure constants
FIG_HEIGHT = 500                      # Height of the Plotly figure in pixels
FIG_WIDTH = 900                       # Width of the Plotly figure in pixels
MARGIN_RATIO = 0.2                    # Ratio for calculating diagram margins
DEFAULT_MARGIN = 0.5                  # Default margin if only one node exists

# Calculation constants
MIDPOINT_FRACTION = 0.5               # Fraction for midpoint calculation in labels

ARROW_STYLE = {
    "showarrow": True,
    "arrowhead": 2,
    "arrowsize": 2,
    "arrowwidth": 1,
    "arrowcolor": "black",
    "axref": "x",
    "ayref": "y"
}


def name_hash(name: str) -> str:
    hobj = hashlib.md5()
    hobj.update(name.encode("UTF-8"))
    return hobj.hexdigest()


def add_arrow_label(
    fig: go.Figure, start: Tuple, end: Tuple,
    ctrl: Optional[Tuple] = None, text: str = "", font_size: int = DEFAULT_FONT_SIZE
):
    """
    Adds a label at the midpoint of a quadratic curve (if ctrl is provided)
    or at the midpoint of a straight line (if ctrl is None).

    Parameters:
        fig (go.Figure): The Plotly figure to add the annotation to.
        start (tuple): (x_start, y_start) coordinates of the arrow's starting point.
        end (tuple): (x_end, y_end) coordinates of the arrow's ending point.
        ctrl (tuple, optional): (ctrl_x, ctrl_y) coordinates of the control point
                                for a quadratic Bézier curve. If None, a straight
                                line is used.
        text (str): The label text to display.
        font_size (int): Font size for the label.
    """
    x_start, y_start = start
    x_end, y_end = end

    if ctrl is not None:
        ctrl_x, ctrl_y = ctrl
        # Quadratic Bézier midpoint
        label_x = (
            (1 - MIDPOINT_FRACTION) ** 2 * x_start +
            2 * (1 - MIDPOINT_FRACTION) * MIDPOINT_FRACTION * ctrl_x +
            MIDPOINT_FRACTION ** 2 * x_end
        )
        label_y = (
            (1 - MIDPOINT_FRACTION) ** 2 * y_start +
            2 * (1 - MIDPOINT_FRACTION) * MIDPOINT_FRACTION * ctrl_y +
            MIDPOINT_FRACTION ** 2 * y_end
        )
    else:
        # Straight line midpoint
        label_x = (x_start + x_end) / 2
        label_y = (y_start + y_end) / 2

    fig.add_annotation(
        x=label_x,
        y=label_y,
        text=text,
        showarrow=False,
        font={"size": font_size, "color": "black"},
        align="center",
        bgcolor="white",
        opacity=OPACITY,
    )


def adjust_endpoint_for_rect(
    start: tuple, end: tuple, half_width: float = 0.1, half_height: float = 0.05
) -> tuple:
    """
    Calculates the intersection point of a line from the start point to the end point
    with the boundary of a rectangle centered at the end point.

    The rectangle is defined by its half-width and half-height.
    The function returns the intersection point on the rectangle's edge in the
    direction from start to end.

    Parameters:
        start (tuple): (x_start, y_start) coordinates of the line's starting point
        (outside the rectangle).
        end (tuple): (x_end, y_end) coordinates of the rectangle's center (target).
        half_width (float): Half the width of the rectangle.
        half_height (float): Half the height of the rectangle.

    Returns:
        tuple: (x_intersect, y_intersect) coordinates of the intersection point on
        the rectangle's edge.
    """
    x_start, y_start = start
    x_end, y_end = end

    # Vector from start to end (center)
    vector_x = x_end - x_start
    vector_y = y_end - y_start

    # Delta from start to center
    delta_center = (x_start - x_end, y_start - y_end)
    delta_x_center, delta_y_center = delta_center

    if vector_x == 0 and vector_y == 0:
        return end

    intersection_params = []
    if vector_x != 0:
        for sign in [-1, 1]:
            param_x = (sign * half_width - delta_x_center) / vector_x
            candidate_y = delta_y_center + param_x * vector_y
            if abs(candidate_y) <= half_height and param_x > 0:
                intersection_params.append(param_x)
    if vector_y != 0:
        for sign in [-1, 1]:
            param_y = (sign * half_height - delta_y_center) / vector_y
            candidate_x = delta_x_center + param_y * vector_x
            if abs(candidate_x) <= half_width and param_y > 0:
                intersection_params.append(param_y)
    if not intersection_params:
        return end
    min_param = min(intersection_params)
    x_intersect = x_start + min_param * vector_x
    y_intersect = y_start + min_param * vector_y
    return (x_intersect, y_intersect)


def prepare_nodes(report):
    """
    Prepare node data and positions for the diagram.

    Parameters:
        report: The report object containing configuration and traceability data.

    Returns:
        node_data: Dict mapping node_id to node data.
        node_positions: Dict mapping node_id to (x, y) positions.
    """

    node_data = {}
    node_positions = {}

    type_levels = {"requirements": [], "implementation": [], "activity": []}

    for level in report.config.values():
        type_levels[level.kind].append(level)
    for type_name, levels in type_levels.items():
        levels_count = len(levels)
        for idx, level in enumerate(levels):
            node_id = f"n_{name_hash(level.name)}"
            x = DEFAULT_NODE_X + (idx - (levels_count - 1) / 2) * NODE_SPACING_X
            y = Y_POSITIONS[type_name]
            node_positions[node_id] = (x, y)
            node_data[node_id] = level
    return node_data, node_positions


def prepare_edges(report):
    """
    Prepare edge data and arrow labels for the diagram.
    """
    edge_pairs = set()
    arrow_labels = {}

    for level in report.config.values():
        source_id = f"n_{name_hash(level.name)}"
        for target_name in getattr(level, "traces", []):
            target_id = f"n_{name_hash(target_name)}"
            edge_pairs.add((source_id, target_id))
            arrow_labels[(source_id, target_id)] = getattr(
                level,
                "arrow_label",
                DEFAULT_ARROW_LABEL)

    edges = []
    for (source_id, target_id) in edge_pairs:
        is_bidirectional = (target_id, source_id) in edge_pairs
        label = arrow_labels.get((source_id, target_id), "")
        if is_bidirectional:
            if source_id < target_id:  # Only add once for bidirectional
                edges.append((source_id, target_id, label, True))
        else:
            edges.append((source_id, target_id, label, False))

    return edges, arrow_labels


def draw_nodes(fig, node_data, node_positions, node_dimensions):
    """
    Draw nodes as rectangles with labels on the Plotly figure.

    Parameters:
        fig: The Plotly figure to draw on.
        node_data: Dict mapping node_id to node data.
        node_positions: Dict mapping node_id to (x, y) positions.
        node_dimensions: Dict to store node_id to (width, height).
    """
    for node_id, level in node_data.items():
        x, y = node_positions[node_id]
        label = level.name
        node_width = max(NODE_MIN_WIDTH, (len(label) * CHAR_WIDTH) + NODE_LABEL_PADDING)
        fig.add_shape(
            type="rect",
            x0=x - node_width / 2, y0=y - NODE_HEIGHT / 2,
            x1=x + node_width / 2, y1=y + NODE_HEIGHT / 2,
            line={"color": "black"},
            fillcolor="white"
        )
        node_dimensions[node_id] = (node_width, NODE_HEIGHT)
        fig.add_annotation(
            x=x, y=y,
            text=label,
            showarrow=False,
            font={"size": NODE_LABEL_FONT_SIZE},
        )


def draw_curved_edge(
        fig,
        source_endpoint,
        target_endpoint,
        curve_offset,
        arrow_label,
        arrow_style,
        shorten_factor):
    """
    Draw a single curved edge with arrowhead and label.

    Parameters:
        fig: The Plotly figure to draw on.
        source_endpoint: (x, y) coordinates where the arrow starts.
        target_endpoint: (x, y) coordinates where the arrow ends.
        curve_offset: Amount of curve perpendicular to the line.
        arrow_label: Text label for the arrow.
        arrow_style: Dictionary of arrow styling parameters.
        shorten_factor: Factor to shorten arrowhead along curve.
    """
    delta_x = target_endpoint[0] - source_endpoint[0]
    delta_y = target_endpoint[1] - source_endpoint[1]
    arrow_length = (delta_x ** 2 + delta_y ** 2) ** 0.5 or 1

    # Calculate perpendicular offset for curve
    perpendicular_offset_x = -delta_y / arrow_length * curve_offset
    perpendicular_offset_y = delta_x / arrow_length * curve_offset

    # Calculate curve control point
    curve_control_point = (
        (source_endpoint[0] + target_endpoint[0]) / 2 + perpendicular_offset_x,
        (source_endpoint[1] + target_endpoint[1]) / 2 + perpendicular_offset_y
    )

    # Calculate arrowhead point (shortened along curve)
    arrowhead_point = (
        curve_control_point[0] *
        (1 - shorten_factor) + target_endpoint[0] *
        shorten_factor,
        curve_control_point[1] *
        (1 - shorten_factor) + target_endpoint[1] *
        shorten_factor
    )

    # Draw curved path
    fig.add_shape(
        type="path",
        path=(
            f"M{source_endpoint[0]},{source_endpoint[1]} "
            f"Q{curve_control_point[0]},{curve_control_point[1]} "
            f"{target_endpoint[0]},{target_endpoint[1]}"
        ),
        line={"color": "black", "width": 1},
        layer="above"
    )

    # Add arrowhead
    fig.add_annotation(
        x=target_endpoint[0], y=target_endpoint[1],
        ax=arrowhead_point[0], ay=arrowhead_point[1],
        **arrow_style
    )

    # Add label
    add_arrow_label(
        fig,
        source_endpoint,
        target_endpoint,
        curve_control_point,
        arrow_label)


def draw_straight_edge(fig, source_endpoint, target_endpoint, arrow_label, arrow_style):
    """
    Draw a single straight edge with arrowhead and label.

    Parameters:
        fig: The Plotly figure to draw on.
        source_endpoint: (x, y) coordinates where the arrow starts.
        target_endpoint: (x, y) coordinates where the arrow ends.
        arrow_label: Text label for the arrow.
        arrow_style: Dictionary of arrow styling parameters.
    """
    # Draw straight arrow
    fig.add_annotation(
        x=target_endpoint[0], y=target_endpoint[1],
        ax=source_endpoint[0], ay=source_endpoint[1],
        **arrow_style
    )

    # Add label
    add_arrow_label(fig, source_endpoint, target_endpoint, text=arrow_label)


def should_curve_edge(source_id, target_id, edges, node_positions):
    """
    Determine if an edge needs to be curved based on competing edges.

    Parameters:
        source_id: Source node ID of the current edge
        target_id: Target node ID of the current edge
        edges: List of all edges [(source_id, target_id, label), ...]
        node_positions: Dict mapping node_id to (x, y) positions

    Returns:
        bool: True if the edge should be curved, False if it should be straight
    """

    # Count edges sharing the same source or target
    competing_edges = []
    for other_source, other_target, _, other_bidirectional in edges:
        if (not other_bidirectional and
            (other_source == source_id or other_target == target_id)):
            # Calculate edge length
            other_source_pos = node_positions[other_source]
            other_target_pos = node_positions[other_target]
            other_length = ((other_target_pos[0] - other_source_pos[0])**2 +
                            (other_target_pos[1] - other_source_pos[1])**2)**0.5
            competing_edges.append((other_length, other_source, other_target))

    # If only one edge (no competition), no curve needed
    if len(competing_edges) <= 1:
        return False

    # Calculate current edge length
    source_pos = node_positions[source_id]
    target_pos = node_positions[target_id]
    delta_x = target_pos[0] - source_pos[0]
    delta_y = target_pos[1] - source_pos[1]
    edge_length = (delta_x ** 2 + delta_y ** 2) ** 0.5

    # Check if this is the shortest edge among competitors
    is_shortest = True
    for other_length, other_source, other_target in competing_edges:
        if ((other_source != source_id or other_target != target_id) and
            other_length < edge_length):
            is_shortest = False
            break

    # Curve if not the shortest (shortest edge stays straight)
    return not is_shortest


def draw_edges(fig, edges, node_positions, node_dimensions, arrow_labels):
    """
    Draw arrows (edges) between nodes on the Plotly figure.

    Parameters:
        fig: The Plotly figure to draw on.
        edges: List of tuples (source_id, target_id, label, bidirectional).
        node_positions: Dict mapping node_id to (x, y) positions.
        node_dimensions: Dict mapping node_id to (width, height).
        arrow_labels: Dict mapping (source_id, target_id) to label.
    """

    for source_id, target_id, arrow_label, bidirectional in edges:
        source_pos = node_positions[source_id]
        target_pos = node_positions[target_id]
        source_dim = node_dimensions[source_id]
        target_dim = node_dimensions[target_id]

        source_endpoint = adjust_endpoint_for_rect(
            source_pos, target_pos,
            half_width=target_dim[0] / 2,
            half_height=target_dim[1] / 2
        )
        target_endpoint = adjust_endpoint_for_rect(
            target_pos, source_pos,
            half_width=source_dim[0] / 2,
            half_height=source_dim[1] / 2
        )

        if bidirectional and source_id < target_id:
            # First arrow: source to target (curved one way)
            draw_curved_edge(
                fig, source_endpoint, target_endpoint,
                ARROW_CURVE_AMOUNT_BIDIRECTIONAL,
                arrow_label, ARROW_STYLE, ARROW_SHORTEN_FACTOR
            )

            # Second arrow: target to source (curved the other way)
            reverse_arrow_label = arrow_labels.get((target_id, source_id), "")
            draw_curved_edge(
                fig, target_endpoint, source_endpoint,
                -ARROW_CURVE_AMOUNT_BIDIRECTIONAL,
                reverse_arrow_label, ARROW_STYLE, ARROW_SHORTEN_FACTOR
            )

        elif not bidirectional:
            need_curve = should_curve_edge(source_id, target_id, edges, node_positions)
            if need_curve:
                draw_curved_edge(
                    fig, source_endpoint, target_endpoint,
                    ARROW_CURVE_AMOUNT_NON_BIDIRECTIONAL,
                    arrow_label, ARROW_STYLE, ARROW_SHORTEN_FACTOR
                )
            else:
                draw_straight_edge(fig, source_endpoint, target_endpoint,
                                   arrow_label, ARROW_STYLE)
        else:
            continue


def add_svg_links(svg_content):
    """
    Post-processes Plotly SVG to wrap each <text class="annotation-text">
    node label with <a xlink:href="...">, where the href is generated as
    f"#sec-{name_hash(label)}".
    """
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
    root = ET.fromstring(svg_content)

    def iter_with_parent(elem):
        for child in elem:
            yield child, elem
            yield from iter_with_parent(child)

    for text_elem, parent in iter_with_parent(root):
        if (text_elem.tag.endswith('text') and
            'annotation-text' in text_elem.attrib.get('class', '')):
            # Try to get label from tspan
            label = None
            for tspan in text_elem.findall('{http://www.w3.org/2000/svg}tspan'):
                if tspan.text and tspan.text.strip():
                    label = tspan.text.strip()
                    break
            if not label and text_elem.text and text_elem.text.strip():
                label = text_elem.text.strip()
            if label:
                section = f"#sec-{name_hash(label)}"
                a_elem = ET.Element('{http://www.w3.org/2000/svg}a', {
                    '{http://www.w3.org/1999/xlink}href': section
                })
                a_elem.append(text_elem)
                for idx, child in enumerate(parent):
                    if child is text_elem:
                        parent[idx] = a_elem
                        break
    svg_str = ET.tostring(root, encoding="unicode")
    # Remove ns0: and :ns0 for browser compatibility
    svg_str = svg_str.replace('ns0:', '').replace(':ns0', '')
    return svg_str


def create_policy_diagram_plotly(doc: htmldoc.Document, report: Report):
    """
    Generates a policy diagram as an interactive Plotly HTML visualization.

    The diagram displays nodes for requirements, implementation, and activities,
    and draws arrows to represent traceability relationships between them.

    Parameters:
        doc (htmldoc.Document): The HTML document object to which the diagram's
        HTML will be added.
        report (Report): The report object containing configuration and
        traceability data.

    The function:
        - Calculates node positions and sizes based on report data.
        - Draws nodes as rectangles with labels.
        - Draws arrows (with optional labels) to show relationships.
        - Handles bidirectional and unidirectional traces.
        - Adds the resulting Plotly HTML to the provided document.
    """
    node_data, node_positions = prepare_nodes(report)
    edges, arrow_labels = prepare_edges(report)

    # Calculate min/max for x and y to fit all nodes and arrows
    all_x = [pos[0] for pos in node_positions.values()]
    all_y = [pos[1] for pos in node_positions.values()]
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    x_margin = (
        (max_x - min_x) * MARGIN_RATIO
        if len(all_x) > 1 else DEFAULT_MARGIN
    )
    y_margin = (
        (max_y - min_y) * MARGIN_RATIO
        if len(all_y) > 1 else DEFAULT_MARGIN
    )

    x_range = [min_x - x_margin, max_x + x_margin]
    y_range = [min_y - y_margin, max_y + y_margin]

    fig = go.Figure()
    node_dimensions = {}

    draw_nodes(fig, node_data, node_positions, node_dimensions)
    draw_edges(fig, edges, node_positions, node_dimensions, arrow_labels)

    # Finalize figure
    fig.update_xaxes(
        visible=False, range=x_range, scaleanchor="y", scaleratio=1
    )
    fig.update_yaxes(visible=False, range=y_range)
    fig.update_layout(
        height=FIG_HEIGHT, width=FIG_WIDTH, plot_bgcolor="white"
    )

    image = fig.to_image(format="svg")
    svg = image.decode("utf-8") if isinstance(image, bytes) else image
    svg_with_links = add_svg_links(svg)
    doc.add_line(svg_with_links)
