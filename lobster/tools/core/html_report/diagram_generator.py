import hashlib
import plotly.graph_objects as go

from lobster.html import htmldoc
from lobster.report import Report

def name_hash(name: str) -> str:
    hobj = hashlib.md5()
    hobj.update(name.encode("UTF-8"))
    return hobj.hexdigest()


def add_arrow_label(
    fig: go.Figure, start: tuple, end: tuple,
    ctrl: tuple = None, text: str = "", font_size: int = 11
):
    """
    Adds a label at the midpoint of a quadratic curve (if ctrl is provided)
    or at the midpoint of a straight line (if ctrl is None).

    Parameters:
        fig (go.Figure): The Plotly figure to add the annotation to.
        start (tuple): (x_start, y_start) coordinates of the arrow's starting point.
        end (tuple): (x_end, y_end) coordinates of the arrow's ending point.
        ctrl (tuple, optional): (ctrl_x, ctrl_y) coordinates of the control point for a quadratic Bézier curve.
        If None, a straight line is used.
        text (str): The label text to display.
        font_size (int): Font size for the label.
    """
    x_start, y_start = start
    x_end, y_end = end
    if ctrl is not None:
        MIDPOINT_FRACTION = 0.5 # Determines that the label is placed at 50% (the middle) between the start and end points.
        ctrl_x, ctrl_y = ctrl
        # Quadratic Bézier midpoint
        label_x = (1 - MIDPOINT_FRACTION) ** 2 * x_start + 2 * (1 - MIDPOINT_FRACTION) * MIDPOINT_FRACTION * ctrl_x + MIDPOINT_FRACTION ** 2 * x_end
        label_y = (1 - MIDPOINT_FRACTION) ** 2 * y_start + 2 * (1 - MIDPOINT_FRACTION) * MIDPOINT_FRACTION * ctrl_y + MIDPOINT_FRACTION ** 2 * y_end
    else:
        # Straight line midpoint
        label_x = (x_start + x_end) / 2
        label_y = (y_start + y_end) / 2

    fig.add_annotation(
        x=label_x, y=label_y,
        text=text,
        showarrow=False,
        font=dict(size=font_size, color="black"),
        align="center",
        bgcolor="white",
        opacity=0.85
    )


def adjust_endpoint_for_rect(
    start: tuple, end: tuple, half_width: float = 0.1, half_height: float = 0.05
) -> tuple:
    """
    Calculates the intersection point of a line from the start point to the end point
    with the boundary of a rectangle centered at the end point.

    The rectangle is defined by its half-width and half-height.
    The function returns the intersection point on the rectangle's edge in the direction from start to end.

    Parameters:
        start (tuple): (x_start, y_start) coordinates of the line's starting point (outside the rectangle).
        end (tuple): (x_end, y_end) coordinates of the rectangle's center (target).
        half_width (float): Half the width of the rectangle.
        half_height (float): Half the height of the rectangle.

    Returns:
        tuple: (x_intersect, y_intersect) coordinates of the intersection point on the rectangle's edge.
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


def create_policy_diagram_plotly(doc: htmldoc.Document, report: Report):
    """
    Generates a policy diagram as an interactive Plotly HTML visualization.

    The diagram displays nodes for requirements, implementation, and activities,
    and draws arrows to represent traceability relationships between them.

    Parameters:
        doc (htmldoc.Document): The HTML document object to which the diagram's HTML will be added.
        report (Report): The report object containing configuration and traceability data.

    The function:
        - Calculates node positions and sizes based on report data.
        - Draws nodes as rectangles with labels.
        - Draws arrows (with optional labels) to show relationships.
        - Handles bidirectional and unidirectional traces.
        - Adds the resulting Plotly HTML to the provided document.
    """

    FIG_HEIGHT = 500                  # Height of the Plotly figure in pixels
    FIG_WIDTH = 900                   # Width of the Plotly figure in pixels

    CHAR_WIDTH = 0.02                 # Estimated width per character for node sizing
    NODE_HEIGHT = 0.2                 # Fixed node height
    NODE_SPACING_X = 0.8              # Horizontal spacing between nodes
    DEFAULT_NODE_X = 0.5              # Default horizontal center for node placement
    NODE_LABEL_FONT_SIZE = 12         # Font size for node labels
    NODE_MIN_WIDTH = 0.28             # Minimum width for node rectangles
    NODE_LABEL_PADDING = 0.1          # Extra padding added to node width for label
    ARROW_CURVE_AMOUNT = 0.08         # Amount of curve for bidirectional arrows
    ARROW_SHORTEN_FACTOR = 0.9        # Factor to shorten arrowhead placement along curve
    MARGIN_RATIO = 0.2                # Ratio for calculating diagram margins
    DEFAULT_MARGIN = 0.5              # Default margin if only one node exists
    DEFAULT_ARROW_LABEL = "trace to"  # Default label for arrows if not specified

    Y_POSITIONS = {"requirements": 1.0, "implementation": 0.6, "activity": 0.2}

    ARROW_STYLE = dict(
        showarrow=True,
        arrowhead=2,
        arrowsize=2,
        arrowwidth=1,
        arrowcolor="black",
        axref="x", ayref="y"
    )

    node_data = {}
    node_dimensions = {}
    node_positions = {}

    # Gather unique levels of each kind for positioning
    kind_levels = {"requirements": [], "implementation": [], "activity": []}
    for level in report.config.values():
        kind_levels[level["kind"]].append(level)

    # Assign positions for each node
    for kind, levels in kind_levels.items():
        levels_number = len(levels)
        for idx, level in enumerate(levels):
            node_id = f"n_{name_hash(level['name'])}"
            x = DEFAULT_NODE_X + (idx - (levels_number - 1) / 2) * NODE_SPACING_X
            y = Y_POSITIONS[kind]
            node_positions[node_id] = (x, y)
            node_data[node_id] = level

    # Collect edges and arrow labels
    edge_pairs = set()
    arrow_labels = {}
    for level in report.config.values():
        source_id = f"n_{name_hash(level['name'])}"
        for target_name in level.get("traces", []):
            target_id = f"n_{name_hash(target_name)}"
            edge_pairs.add((source_id, target_id))
            arrow_labels[(source_id, target_id)] = level.get("arrow_label", DEFAULT_ARROW_LABEL)

    edges = []
    for (source_id, target_id) in edge_pairs:
        is_bidirectional = (target_id, source_id) in edge_pairs
        label = arrow_labels.get((source_id, target_id), "")
        if is_bidirectional:
            if source_id < target_id:
                edges.append((source_id, target_id, label, True))
        else:
            edges.append((source_id, target_id, label, False))

    # Calculate min/max for x and y to fit all nodes and arrows
    all_x = [pos[0] for pos in node_positions.values()]
    all_y = [pos[1] for pos in node_positions.values()]
    x_margin = (max(all_x) - min(all_x)) * MARGIN_RATIO if len(all_x) > 1 else DEFAULT_MARGIN
    y_margin = (max(all_y) - min(all_y)) * MARGIN_RATIO if len(all_y) > 1 else DEFAULT_MARGIN

    x_range = [min(all_x) - x_margin, max(all_x) + x_margin]
    y_range = [min(all_y) - y_margin, max(all_y) + y_margin]

    fig = go.Figure()

    # Draw nodes (always as rectangles)
    for node_id, level in node_data.items():
        x, y = node_positions[node_id]
        label = level["name"]
        node_width = max(NODE_MIN_WIDTH, (len(label) * CHAR_WIDTH) + NODE_LABEL_PADDING)
        node_height = NODE_HEIGHT

        fig.add_shape(
            type="rect",
            x0=x - node_width / 2, y0=y - node_height / 2,
            x1=x + node_width / 2, y1=y + node_height / 2,
            line=dict(color="black"),
            fillcolor="white"
        )

        node_dimensions[node_id] = (node_width, node_height)

        fig.add_annotation(
            x=x, y=y,
            text=f'<span section="#sec-{name_hash(label)}">{label}</span>',
            showarrow=False,
            font=dict(size=NODE_LABEL_FONT_SIZE),
            hovertext=f"#sec-{name_hash(label)}",
            hoverlabel=dict(bgcolor="white"),
        )

    # Draw arrows
    for source_id, target_id, arrow_label, bidirectional in edges:
        source_pos = node_positions[source_id]
        target_pos = node_positions[target_id]
        source_dim = node_dimensions[source_id]
        target_dim = node_dimensions[target_id]

        target_endpoint = adjust_endpoint_for_rect(
            source_pos, target_pos, half_width=target_dim[0] / 2, half_height=target_dim[1] / 2
        )
        source_endpoint = adjust_endpoint_for_rect(
            target_pos, source_pos, half_width=source_dim[0] / 2, half_height=source_dim[1] / 2
        )

        if bidirectional and source_id < target_id:
            # Curve amount for separation
            curve = ARROW_CURVE_AMOUNT
            delta_x_arrow = source_endpoint[0] - target_endpoint[0]
            delta_y_arrow = source_endpoint[1] - target_endpoint[1]
            arrow_length = (delta_x_arrow ** 2 + delta_y_arrow ** 2) ** 0.5 or 1
            perpendicular_offset_x = -delta_y_arrow / arrow_length * curve
            perpendicular_offset_y = delta_x_arrow / arrow_length * curve

            # Arrow from target to source (curved one way)
            curve_control_point_1 = ((target_endpoint[0] + source_endpoint[0]) / 2 + perpendicular_offset_x,
                     (target_endpoint[1] + source_endpoint[1]) / 2 + perpendicular_offset_y)
            shorten = ARROW_SHORTEN_FACTOR
            arrowhead_point_1 = (curve_control_point_1[0] * (1 - shorten) + source_endpoint[0] * shorten,
                          curve_control_point_1[1] * (1 - shorten) + source_endpoint[1] * shorten)

            fig.add_shape(
                type="path",
                path=f"M{target_endpoint[0]},{target_endpoint[1]} Q{curve_control_point_1[0]},{curve_control_point_1[1]} {source_endpoint[0]},{source_endpoint[1]}",
                line=dict(color="black", width=1),
                layer="above"
            )
            fig.add_annotation(
                x=source_endpoint[0], y=source_endpoint[1],
                ax=arrowhead_point_1[0], ay=arrowhead_point_1[1],
                **ARROW_STYLE
            )

            # Arrow from source to target (curved the other way)
            curve_control_point_2 = ((target_endpoint[0] + source_endpoint[0]) / 2 - perpendicular_offset_x,
                     (target_endpoint[1] + source_endpoint[1]) / 2 - perpendicular_offset_y)
            reverse_arrow_label = arrow_labels.get((target_id, source_id), "")
            arrowhead_point_2 = (curve_control_point_2[0] * (1 - shorten) + target_endpoint[0] * shorten,
                          curve_control_point_2[1] * (1 - shorten) + target_endpoint[1] * shorten)

            fig.add_shape(
                type="path",
                path=f"M{source_endpoint[0]},{source_endpoint[1]} Q{curve_control_point_2[0]},{curve_control_point_2[1]} {target_endpoint[0]},{target_endpoint[1]}",
                line=dict(color="black", width=1),
                layer="above"
            )
            fig.add_annotation(
                x=target_endpoint[0], y=target_endpoint[1],
                ax=arrowhead_point_2[0], ay=arrowhead_point_2[1],
                **ARROW_STYLE
            )

            add_arrow_label(fig, target_endpoint, source_endpoint, curve_control_point_1, arrow_label)
            add_arrow_label(fig, source_endpoint, target_endpoint, curve_control_point_2, reverse_arrow_label)

        elif not bidirectional:
            fig.add_annotation(
                x=source_endpoint[0], y=source_endpoint[1],
                ax=target_endpoint[0], ay=target_endpoint[1],
                **ARROW_STYLE
            )
            add_arrow_label(fig, target_endpoint, source_endpoint, text=arrow_label)
        else:
            continue

    # Finalize figure
    fig.update_xaxes(visible=False, range=x_range, scaleanchor="y", scaleratio=1)
    fig.update_yaxes(visible=False, range=y_range)
    fig.update_layout(height=FIG_HEIGHT, width=FIG_WIDTH, plot_bgcolor="white")

    # Convert to HTML fragment
    html_fragment = fig.to_html(full_html=True, include_plotlyjs="cdn")
    for line in html_fragment.splitlines():
        doc.add_line(line)
