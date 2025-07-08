import hashlib
import tempfile
import plotly.graph_objects as go
import subprocess
import os.path

from lobster.html import htmldoc
from lobster.report import Report

def name_hash(name):
    hobj = hashlib.md5()
    hobj.update(name.encode("UTF-8"))
    return hobj.hexdigest()


def create_policy_diagram_dot(doc, report, dot):
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
        svg = subprocess.run([dot if dot else "dot", "-Tsvg", graph_name],
                             stdout=subprocess.PIPE,
                             encoding="UTF-8",
                             check=True)
        assert svg.returncode == 0
        image = svg.stdout[svg.stdout.index("<svg "):]

    for line in image.splitlines():
        doc.add_line(line)


def add_arrow_label(fig, x0, y0, x1, y1, ctrl_x=None, ctrl_y=None, text="", font_size=11):
    """
    Adds a label at the midpoint of a quadratic Bézier curve (or straight line if ctrl_x/y is None).
    """
    t = 0.5
    if ctrl_x is not None and ctrl_y is not None:
        # Quadratic Bézier midpoint
        label_x = (1 - t)**2 * x0 + 2 * (1 - t) * t * ctrl_x + t**2 * x1
        label_y = (1 - t)**2 * y0 + 2 * (1 - t) * t * ctrl_y + t**2 * y1
    else:
        # Straight line midpoint
        label_x = (x0 + x1) / 2
        label_y = (y0 + y1) / 2

    fig.add_annotation(
        x=label_x, y=label_y,
        text=text,
        showarrow=False,
        font=dict(size=font_size, color="black"),
        align="center",
        bgcolor="white",
        opacity=0.85
    )

# helper function to adjust arrow endpoint to node edge (rectangles and diamonds)
def adjust_endpoint_for_rect(x_start, y_start, x_end, y_end, hw=0.1, hh=0.05):
    """
    Returns the intersection point of the line from (x_start, y_start) to (x_end, y_end)
    with the rectangle centered at (x_end, y_end) with half-width hw and half-height hh.
    """
    cx, cy = x_end, y_end
    dx = x_start - cx
    dy = y_start - cy
    vx = x_end - x_start
    vy = y_end - y_start

    # Avoid division by zero
    if vx == 0 and vy == 0:
        return cx, cy

    # Calculate intersection with each side
    t_values = []
    if vx != 0:
        for sign in [-1, 1]:
            tx = (sign * hw - dx) / vx
            y = dy + tx * vy
            if abs(y) <= hh and tx > 0:
                t_values.append(tx)
    if vy != 0:
        for sign in [-1, 1]:
            ty = (sign * hh - dy) / vy
            x = dx + ty * vx
            if abs(x) <= hw and ty > 0:
                t_values.append(ty)
    if not t_values:
        return cx, cy
    t = min(t_values)
    x_adj = x_start + t * vx
    y_adj = y_start + t * vy
    return x_adj, y_adj

def adjust_endpoint_for_ellipse(x_start, y_start, x_end, y_end, a, b):
    """
    Adjust the endpoint (x_end, y_end) so that the line from (x_start, y_start) to (x_end, y_end)
    intersects the ellipse centered at (cx, cy) = (x_end, y_end) with radii a (x) and b (y).
    Returns the intersection point on the ellipse boundary, starting from (x_start, y_start).
    """
    cx, cy = x_end, y_end
    dx = x_start - cx
    dy = y_start - cy

    vx = x_end - x_start
    vy = y_end - y_start

    A = (vx*vx)/(a*a) + (vy*vy)/(b*b)
    B = 2*((dx*vx)/(a*a) + (dy*vy)/(b*b))
    C = (dx*dx)/(a*a) + (dy*dy)/(b*b) - 1

    discriminant = B*B - 4*A*C
    if discriminant < 0 or A == 0:
        return cx, cy
    sqrt_disc = discriminant**0.5
    t1 = (-B + sqrt_disc) / (2*A)
    t2 = (-B - sqrt_disc) / (2*A)

    t_candidates = [t for t in (t1, t2) if t > 0]
    if not t_candidates:
        return cx, cy
    t = min(t_candidates)
    x_adj = x_start + t * vx
    y_adj = y_start + t * vy
    return x_adj, y_adj


def get_adjusted_endpoint(kind, x0, y0, x1, y1, w, h):
    """
    Calculate the intersection point of a line with the edge of a node shape.

    Given a node of a certain kind (e.g., "requirements", "implementation", "activity") centered at (x1, y1)
    with width w and height h, this function computes the intersection point between the node's boundary
    and the line from (x0, y0) to (x1, y1). This is typically used to ensure arrows start or end exactly
    at the edge of the node shape, not at its center.

    Parameters:
        kind (str): The kind of node ("requirements" for ellipse, others for rectangle/diamond).
        x0, y0 (float): The coordinates of the point outside the node (usually the other node's center).
        x1, y1 (float): The coordinates of the node center whose edge is being computed.
        w (float): The width of the node.
        h (float): The height of the node.

    Returns:
        (float, float): The (x, y) coordinates of the intersection point on the node's edge.
    """
    if kind == "requirements":
        return adjust_endpoint_for_ellipse(x0, y0, x1, y1, w/2, h/2)
    else:
        return adjust_endpoint_for_rect(x0, y0, x1, y1, hw=w/2, hh=h/2)


def create_policy_diagram_plotly(doc, report):
    nodes = {}
    edges = []
    node_dims = {}

    # collect positions dynamically
    positions = {}
    spacing_x = 0.8  # horizontal spacing

    # gather unique levels of each kind for positioning
    kind_levels = {"requirements": [], "implementation": [], "activity": []}
    for level in report.config.values():
        kind_levels[level["kind"]].append(level)

    # assign y levels (higher is earlier)
    y_map = {"requirements": 1.0, "implementation": 0.6, "activity": 0.2}
    for kind, levels in kind_levels.items():
        n = len(levels)
        for idx, level in enumerate(levels):
            node_id = f"n_{name_hash(level['name'])}"
            # evenly space horizontally
            x = 0.5 + (idx - (n - 1) / 2) * spacing_x
            y = y_map[kind]
            positions[node_id] = (x, y)
            nodes[node_id] = level

    # collect edges
    edge_pairs = set()
    arrow_labels = {}
    for level in report.config.values():
        source = f"n_{name_hash(level['name'])}"
        for target_name in level.get("traces", []):
            target = f"n_{name_hash(target_name)}"
            edge_pairs.add((source, target))
            arrow_labels[(source, target)] = level.get("arrow_label", "trace to")

    edges = []
    for (source, target) in edge_pairs:
        is_bidir = (target, source) in edge_pairs
        label = arrow_labels.get((source, target), "")
        if is_bidir:
            if source < target:
                edges.append((source, target, label, True))
        else:
            edges.append((source, target, label, False))

    # Calculate min/max for x and y to fit all nodes and arrows
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    x_margin = (max(all_x) - min(all_x)) * 0.2 if len(all_x) > 1 else 0.5
    y_margin = (max(all_y) - min(all_y)) * 0.2 if len(all_y) > 1 else 0.5

    x_range = [min(all_x) - x_margin, max(all_x) + x_margin]
    y_range = [min(all_y) - y_margin, max(all_y) + y_margin]

    fig = go.Figure()

    # draw nodes
    for node_id, level in nodes.items():
        x, y = positions[node_id]
        label = level["name"]

        # Estimate node width based on label length
        char_width = 0.02  # tweak this value for your font/scale
        node_width = max(0.28, (len(label) * char_width) + 0.1)  # ensure minimum width
        node_height = 0.2  # keep height fixed or adjust as needed

        if level["kind"] == "requirements":
            # Draw an oval (ellipse) using type="circle" with different width/height
            fig.add_shape(
                type="circle",
                x0=x - node_width/2, y0=y - node_height/2,
                x1=x + node_width/2, y1=y + node_height/2,
                line=dict(color="black"),
                fillcolor="white"
            )
        elif level["kind"] == "implementation":
            # Rectangle (box)
            fig.add_shape(
                type="rect",
                x0=x - node_width/2, y0=y - node_height/2,
                x1=x + node_width/2, y1=y + node_height/2,
                line=dict(color="black"),
                fillcolor="white"
            )
        else:
            assert level["kind"] == "activity"
            # Diamond (as before)
            node_width = node_width + 0.1
            diamond_path = (
                f"M{x},{y + node_height/2} "
                f"L{x + node_width/2},{y} "
                f"L{x},{y - node_height/2} "
                f"L{x - node_width/2},{y} Z"
            )
            fig.add_shape(type="path", path=diamond_path,
                        line=dict(color="black"), fillcolor="white")

        node_dims[node_id] = (node_width, node_height)

        fig.add_annotation(
            x=x, y=y, text=label, showarrow=False,
            font=dict(size=12)
        )

    # draw arrows, adjusting end points to node edges
    for source, target, arrow_label, bidirectional in edges:
        x0, y0 = positions[source]
        x1, y1 = positions[target]

        node_width_t, node_height_t = node_dims[target]
        node_width_s, node_height_s = node_dims[source]

        # For target
        x1_adj, y1_adj = get_adjusted_endpoint(nodes[target]["kind"], x0, y0, x1, y1, node_width_t, node_height_t)
        # For source
        x0_adj, y0_adj = get_adjusted_endpoint(nodes[source]["kind"], x1, y1, x0, y0, node_width_s, node_height_s)

        arrow_style = dict(
            showarrow=True,
            arrowhead=2,
            arrowsize=2,
            arrowwidth=1,
            arrowcolor="black",
            axref="x", ayref="y"
        )

        if bidirectional and source < target:  # Only draw each pair once, both directions
            # Curve amount for separation
            curve = 0.08

            dx = x1_adj - x0_adj
            dy = y1_adj - y0_adj
            norm = (dx**2 + dy**2) ** 0.5 or 1
            perp_x = -dy / norm * curve
            perp_y = dx / norm * curve

            # Arrow from source to target (curved one way)
            ctrl1_x = (x0_adj + x1_adj) / 2 + perp_x
            ctrl1_y = (y0_adj + y1_adj) / 2 + perp_y
            # Shorten the arrowhead by interpolating between control and end
            shorten = 0.9  # 0 = arrowhead at control point, 1 = at end, 0.3 = closer to end
            ax1 = ctrl1_x * (1 - shorten) + x1_adj * shorten
            ay1 = ctrl1_y * (1 - shorten) + y1_adj * shorten

            fig.add_shape(
                type="path",
                path=f"M{x0_adj},{y0_adj} Q{ctrl1_x},{ctrl1_y} {x1_adj},{y1_adj}",
                line=dict(color="black", width=1),
                layer="above"
            )
            fig.add_annotation(
                x=x1_adj, y=y1_adj,
                ax=ax1, ay=ay1,
                **arrow_style
            )

            # Arrow from target to source (curved the other way)
            ctrl2_x = (x0_adj + x1_adj) / 2 - perp_x
            ctrl2_y = (y0_adj + y1_adj) / 2 - perp_y
            rev_label = arrow_labels.get((target, source), "")
            ax2 = ctrl2_x * (1 - shorten) + x0_adj * shorten
            ay2 = ctrl2_y * (1 - shorten) + y0_adj * shorten

            fig.add_shape(
                type="path",
                path=f"M{x1_adj},{y1_adj} Q{ctrl2_x},{ctrl2_y} {x0_adj},{y0_adj}",
                line=dict(color="black", width=1),
                layer="above"
            )
            fig.add_annotation(
                x=x0_adj, y=y0_adj,
                ax=ax2, ay=ay2,
                **arrow_style
            )

            add_arrow_label(fig, x0_adj, y0_adj, x1_adj, y1_adj, ctrl1_x, ctrl1_y, arrow_label)
            add_arrow_label(fig, x1_adj, y1_adj, x0_adj, y0_adj, ctrl2_x, ctrl2_y, rev_label)

        elif not bidirectional:
            fig.add_annotation(
                x=x1_adj, y=y1_adj,
                ax=x0_adj, ay=y0_adj,
                **arrow_style
            )
            add_arrow_label(fig, x0_adj, y0_adj, x1_adj, y1_adj, text=arrow_label)
        else:
            # If bidirectional but already drawn, skip this one
            continue

    # finalize figure
    fig.update_xaxes(visible=False, range=x_range, scaleanchor="y", scaleratio=1)
    fig.update_yaxes(visible=False, range=y_range)
    fig.update_layout(height=500, width=900, plot_bgcolor="white")  # wider width

    # convert to HTML fragment
    html_fragment = fig.to_html(full_html=False)

    for line in html_fragment.splitlines():
        doc.add_line(line)